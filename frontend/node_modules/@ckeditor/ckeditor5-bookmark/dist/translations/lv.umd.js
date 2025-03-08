/**
 * @license Copyright (c) 2003-2025, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-licensing-options
 */

( e => {
const { [ 'lv' ]: { dictionary, getPluralForm } } = {"lv":{"dictionary":{"Bookmark":"Grāmatzīme","Insert":"Ievietot","Update":"Atjaunināt","Edit bookmark":"Rediģēt grāmatzīmi","Remove bookmark":"Aizvākt grāmatzīmi","Bookmark name":"Grāmatzīmes nosaukums","Enter the bookmark name without spaces.":"Ievadiet grāmatzīmes nosaukumu bez atstarpēm.","Bookmark must not be empty.":"Grāmatzīmes lauks nedrīkst būt tukšs.","Bookmark name cannot contain space characters.":"Grāmatzīmes nosaukumā nedrīkst būt atstarpes.","Bookmark name already exists.":"Šāds grāmatzīmes nosaukums jau pastāv.","bookmark widget":"grāmatzīmju ikona"},getPluralForm(n){return (n % 10 == 1 && n % 100 != 11 ? 0 : n != 0 ? 1 : 2);}}};
e[ 'lv' ] ||= { dictionary: {}, getPluralForm: null };
e[ 'lv' ].dictionary = Object.assign( e[ 'lv' ].dictionary, dictionary );
e[ 'lv' ].getPluralForm = getPluralForm;
} )( window.CKEDITOR_TRANSLATIONS ||= {} );
