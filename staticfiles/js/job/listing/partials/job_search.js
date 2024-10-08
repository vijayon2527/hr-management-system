$("#id_search").autocomplete({
    source: function (request, response) {
        $.getJSON("/search/", {
            term: extractLast(request.term)
        }, response);
    },
    search: function () {
        // custom minLength
        var term = extractLast(this.value);
        if (term.length < 1) {
            return false;
        }
    },
    focus: function () {
        // prevent value inserted on focus
        return false;
    },
    select: function (event, ui) {
        var terms = split(this.value);
        // remove the current input
        terms.pop();
        // add the selected item
        terms.push(ui.item.value);
        // add placeholder to get the comma-and-space at the end
        terms.push("");
        this.value = terms.join(", ");
        return false;
    }
});
function split(val) {
    return val.split(/,\s*/);
}
function extractLast(term) {
    return split(term).pop();
}

$("#id_location").autocomplete({
  source: function (request, response) {
      $.getJSON("/search/", {
        location: extractLast(request.term)
      }, response);
  },
  search: function () {
      // custom minLength
      var location = extractLast(this.value);
      if (location.length < 1) {
          return false;
      }
  },
  focus: function () {
      // prevent value inserted on focus
      return false;
  },
  select: function (event, ui) {
      var locations = split(this.value);
      // remove the current input
      locations.pop();
      // add the selected item
      locations.push(ui.item.value);
      // add placeholder to get the comma-and-space at the end
      locations.push("");
      this.value = locations.join(", ");
      return false;
  }
});
function split(val) {
  return val.split(/,\s*/);
}
function extractLast(location) {
  return split(location).pop();
}

$("#id_search_form").validate({
	rules:{
		skills:{
			required:true,
		},
        locations:{
			required:true,
		},
	},messages:{
		skills:{
			required:"Please enter skill or job title",
			},
        locations:{
        required:"Please enter place, locality",
        },
	},
})