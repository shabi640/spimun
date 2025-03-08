/**
 * @license Copyright (c) 2003-2025, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-licensing-options
 */

( e => {
const { [ 'no' ]: { dictionary, getPluralForm } } = {"no":{"dictionary":{"Bookmark":"Bokmerk","Insert":"Sett inn","Update":"Oppdater","Edit bookmark":"Rediger bokmerke","Remove bookmark":"Fjern bokmerke","Bookmark name":"Navn på bokmerke","Enter the bookmark name without spaces.":"Oppgi bokmerkets navn uten mellomrom.","Bookmark must not be empty.":"Bokmerket kan ikke være tomt.","Bookmark name cannot contain space characters.":"Bokmerkets navn kan ikke inneholde mellomrom.","Bookmark name already exists.":"Bokmerkets navn finnes allerede.","bookmark widget":"bokmerke-widget"},getPluralForm(n){return (n != 1);}}};
e[ 'no' ] ||= { dictionary: {}, getPluralForm: null };
e[ 'no' ].dictionary = Object.assign( e[ 'no' ].dictionary, dictionary );
e[ 'no' ].getPluralForm = getPluralForm;
} )( window.CKEDITOR_TRANSLATIONS ||= {} );
