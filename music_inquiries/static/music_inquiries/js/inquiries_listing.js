const addResultsToSearchResultsList = (searchResults) => {
  const searchResultsList = $('#inquiry_listing');
  searchResultsList.empty();

  if (searchResults.length > 0) {
    $.each(searchResults, (i, searchResult) => {
      const inquiryUrl = searchResult.url;
      const inquiryText = searchResult.text;
      const numberSuggestons = searchResult.number_of_suggestions;

      const listEntry = $('<li class="inquiry_listing_entry">');

      const linkEntry = $('<a>');
      linkEntry.attr('class', 'inquiry_listing_entry_link');
      linkEntry.attr('href', inquiryUrl);
      linkEntry.text(inquiryText);

      const nSuggestionsDiv = $('<div>');
      nSuggestionsDiv.attr('class', 'inquiry_listing_entry_number_suggestions');
      nSuggestionsDiv.text(`${numberSuggestons} Suggestions`);

      listEntry.append(linkEntry);
      listEntry.append(nSuggestionsDiv);

      searchResultsList.append(listEntry);
    });
  }
};


$(() => {
  $('#search-inquiry-input').keyup(() => {
    const input = $('#search-inquiry-input').val();
    const data = { q: input };
    $.get('/iapi/inquiry/search', data, (searchResults) => {
      addResultsToSearchResultsList(searchResults);
    });
  });
});
