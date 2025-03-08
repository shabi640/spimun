/**
 * @license Copyright (c) 2003-2025, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-licensing-options
 */

( e => {
const { [ 'el' ]: { dictionary, getPluralForm } } = {"el":{"dictionary":{"Bookmark":"Σελιδοδείκτης","Insert":"Εισαγωγή","Update":"Ενημέρωση","Edit bookmark":"Επεξεργασία σελιδοδείκτη","Remove bookmark":"Κατάργηση σελειδοδείκτη","Bookmark name":"Όνομα σελιδοδείκτη","Enter the bookmark name without spaces.":"Εισαγάγετε το όνομα του σελιδοδείκτη χωρίς κενά.","Bookmark must not be empty.":"Ο σελιδοδείκτης δεν πρέπει να είναι κενός.","Bookmark name cannot contain space characters.":"Το όνομα του σελιδοδείκτη δεν μπορεί να περιέχει χαρακτήρες κενού διαστήματος.","Bookmark name already exists.":"Το όνομα σελιδοδείκτη υπάρχει ήδη.","bookmark widget":"widget σελιδοδείκτη"},getPluralForm(n){return (n != 1);}}};
e[ 'el' ] ||= { dictionary: {}, getPluralForm: null };
e[ 'el' ].dictionary = Object.assign( e[ 'el' ].dictionary, dictionary );
e[ 'el' ].getPluralForm = getPluralForm;
} )( window.CKEDITOR_TRANSLATIONS ||= {} );
