#!/usr/bin/python
#
# -*- coding: utf-8 -*-
# Copyright 2019 SAP SE or an SAP affiliate company. All rights reserved
# ============================================================================

import operator
from collections import Counter
from typing import List, Tuple

import pandas as pd

from xai.data.exceptions import ColumnNotFound


class DataframeValidator:

    @classmethod
    def duplication_check(cls, df: pd.DataFrame, key_col: List[str] = None):
        """
        Return duplicated indices in group based on column names

        Args:
            df: dataframe to check
            key_col: a list of column names to check the duplicates

        Returns:
            A list of list with all duplicated row index

        """
        if key_col is None:
            key_col = df.columns
        else:
            for col in key_col:
                if col not in df.columns:
                    raise ColumnNotFound(col, df.columns)
        groups = df.groupby(by=key_col).groups
        results = list()
        for indices in groups.values():
            if len(indices) > 1:
                results.append(indices.to_list())
        return results

    @classmethod
    def orphaned_relation_check(cls, df_a: pd.DataFrame, df_b: pd.DataFrame, col_a: str, col_b: str) -> List[bool]:
        """
        Return all the indices of dataframe A that column a not in column b of dataframe B

        Args:
            df_a: dataframe A
            df_b: dataframe B
            col_a: column name a
            col_b: column name b

        Returns:
            A list of indices that is orphaned
        """

        if col_a not in df_a.columns:
            raise ColumnNotFound(col_a, df_a.columns)
        if col_b not in df_b.columns:
            raise ColumnNotFound(col_b, df_b.columns)
        foreign_key = set(df_b[col_b].values)

        return df_a[~df_a[col_a].isin(foreign_key)].index.tolist()

    @classmethod
    def unidirectional_matches(cls, df_a: pd.DataFrame, df_b: pd.DataFrame, col_a: str, col_b: str) -> List[int]:
        """
        Return for each value in column a [of dataframe A] return the number of its occurrence in column b [of dataframe B]

        Args:
            df_a: dataframe A
            df_b: dataframe B
            col_a: column name a
            col_b: column name b

        Returns:
            A list of number indicates occurrences
        """
        if col_a not in df_a.columns:
            raise ColumnNotFound(col_a, df_a.columns)
        if col_b not in df_b.columns:
            raise ColumnNotFound(col_b, df_b.columns)

        counter_b = Counter(df_b[col_b].values)
        occurrences_count = []
        for value in df_a[col_a].values:
            if value not in counter_b.keys():
                occurrences_count.append(0)
            else:
                occurrences_count.append(counter_b[value])
        return occurrences_count

    @classmethod
    def find_m_to_n_complete_matches(cls, df: pd.DataFrame, col_a: str, col_b: str) -> List[
        Tuple[List[int], List[int]]]:
        """
        Find completed matches between two entities

        Args:
            df: dataframe
            col_a: column name a
            col_b: column name b

        Returns:
            A list of tuple, each item is the indices of nodes in the completed graph
        """
        processed_cols = [col_a, col_b]
        copy_df = df[processed_cols].copy(deep=True)
        copy_df = copy_df.drop_duplicates()
        sorted_unique_a_set = [a for a, _ in
                               sorted(copy_df[col_a].value_counts().items(), key=operator.itemgetter(1))[::-1]]
        matches_found = []
        processed_a = set()

        for idx, value_a in enumerate(sorted_unique_a_set):
            if value_a in processed_a:
                continue
            b_set = set(copy_df[copy_df[col_a] == value_a][col_b].values)  # find all the connected b
            relevant_b = copy_df[col_b].isin(b_set)
            back_a_set = set(copy_df[relevant_b][col_a].values)  # find all the connected a for all the b above
            relevant_a = copy_df[col_a].isin(back_a_set)
            back_b_set = set(copy_df[relevant_a][col_b].values)  # find all the connected b for all the a above
            if len(b_set) == len(back_b_set) and b_set == back_b_set:
                m = len(back_a_set)
                n = len(back_b_set)
                logic = relevant_a & relevant_b
                relevant_mr = copy_df[logic]
                copy_df = copy_df[~logic]
                if len(relevant_mr) == m * n:
                    matches_found.append([list(back_a_set), list(back_b_set)])
            processed_a.update(back_a_set)

        return matches_found

    @classmethod
    def relational_filter(cls, df: pd.DataFrame, relation_query: str):
        """
        Check whether the query is satisfied

        Args:
            df: dataframe
            relation_query: a relational query returns a bool

        Returns:
            A list of true indices
        """

        valid_df = df.query(relation_query)
        return valid_df.index.to_list()
