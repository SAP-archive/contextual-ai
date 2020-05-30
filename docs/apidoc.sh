
# sphinx-apidoc ../xai -o source/ -f -e -M -d 2

sphinx-apidoc ../xai/data -o source/data/ -f -e -M -d 2
sphinx-apidoc ../xai/explainer -o source/explainer/ -f -e -M -d 2
sphinx-apidoc ../xai/formatter -o source/formatter/ -f -e -M -d 2
sphinx-apidoc ../xai/model -o source/model/ -f -e -M -d 2
sphinx-apidoc ../xai/compiler -o source/compiler/ -f -e -M -d 2



make clean
make html

./copy_images.sh


