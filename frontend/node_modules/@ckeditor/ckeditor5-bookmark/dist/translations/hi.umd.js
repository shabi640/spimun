/**
 * @license Copyright (c) 2003-2025, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-licensing-options
 */

( e => {
const { [ 'hi' ]: { dictionary, getPluralForm } } = {"hi":{"dictionary":{"Bookmark":"बुकमार्क","Insert":"इंसर्ट","Update":"अपडेट","Edit bookmark":"बुकमार्क एडिट करें","Remove bookmark":"बुकमार्क हटाएं","Bookmark name":"बुकमार्क का नाम","Enter the bookmark name without spaces.":"बिना स्पेस के बुकमार्क का नाम लिखें.","Bookmark must not be empty.":"बुकमार्क खाली नहीं होना चाहिए.","Bookmark name cannot contain space characters.":"बुकमार्क नाम में स्पेस नहीं हो सकते.","Bookmark name already exists.":"बुकमार्क नाम पहले से मौजूद है.","bookmark widget":"बुकमार्क विजिट"},getPluralForm(n){return (n != 1);}}};
e[ 'hi' ] ||= { dictionary: {}, getPluralForm: null };
e[ 'hi' ].dictionary = Object.assign( e[ 'hi' ].dictionary, dictionary );
e[ 'hi' ].getPluralForm = getPluralForm;
} )( window.CKEDITOR_TRANSLATIONS ||= {} );
