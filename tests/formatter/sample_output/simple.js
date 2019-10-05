   function Section(evt, sectionName) {
      var i, tabcontent, tablinks;
      tabcontent = document.getElementsByClassName("tab_contents");
      for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
      }
      tablinks = document.getElementsByClassName("tab_links");
      for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
      }
      document.getElementById(sectionName).style.display = "block";
      evt.currentTarget.className += " active";
    }