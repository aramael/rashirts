/**
* # Popup Window Helpers
*
* This file contains client-side Javascript that adds
* some additional functionality for opening popup windows.
*
* Other than simply including this file in a page, no further action
* is neccessary to enable this functionality.
*/

//
/*jshint browser:true jquery:true */
$(function() {
  /**
  * When any `a` tag with a `rel` attribute of "popup" is clicked, the
  * browser will open a new window and load the URL specified by
  * the `href` attribute.
  *
  * Additional options to pass to `window.open` can be specified
  * in the following [data attributes][data]:
  *
  * * `data-popup-name`    - A _String_ that represents the name of the new window.
  * * `data-popup-options` - A comma-delimited _String_ that specifies different window options like
  *                          width, height, scroll bar availability, etc.
  *                          For more information on the available options, check
  *                          out the `window.open` entry on the
  *                          [Mozilla Developer Network][mdn].
  *
  * Example link markup:
  *
  *     <a href="http://example.com" rel="popup" data-popup-name="MyPopup" data-popup-options="width=400,height=200,scrollbars=no">Open</a>
  *
  */
  $(document).delegate('a[rel=popup]', 'click', function(e) {
    e.preventDefault();

    var link = $(this),
        url = link.attr('href'),
        name = link.attr('data-popup-name'),
        options = link.attr('data-popup-options');

    if (!window.name || window.name.length === 0) { window.name = 'customink-main'; }

    window.open(url, name, options);
  });
});

/**
* [data]: http://www.whatwg.org/specs/web-apps/current-work/multipage/elements.html#custom-data-attribute
* [mdn]: http://developer.mozilla.org/En/Window.open
*/
