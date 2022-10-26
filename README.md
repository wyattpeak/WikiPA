# H2O.Today and WikiPA

## Installation

### Wiki setup

To set up the wiki:

1. Install a MediaWiki instance according to [their instructions](https://www.mediawiki.org/wiki/Manual:Installing_MediaWiki).
2. Extract the file `wiki_resouces/mediawiki-extensions-PageForms-5.4.tar.gz` to the `extensions` directory of your MediaWiki instance.
3. At the end of `LocalSettings.php`, add the line `wfLoadExtension( 'PageForms' );`.
4. Add the pages in `wiki_resouces/pages` to your wiki:
	1. The contents of `template_request.html` should be added to the page "Template:Request"
	2. The contents of `form_request.html` should be added to the page "Form:Request"
	3. The contents of `category_requests.html` should be added to the page "Category:Requests"