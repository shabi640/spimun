/**
 * @license Copyright (c) 2003-2025, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-licensing-options
 */

( e => {
const { [ 'th' ]: { dictionary, getPluralForm } } = {"th":{"dictionary":{"Bookmark":"บุ๊กมาร์ก","Insert":"แทรก","Update":"อัปเดต","Edit bookmark":"แก้ไขบุ๊กมาร์ก","Remove bookmark":"ลบบุ๊กมาร์ก","Bookmark name":"ชื่อบุ๊กมาร์ก","Enter the bookmark name without spaces.":"ป้อนชื่อบุ๊กมาร์กโดยไม่มีช่องว่าง","Bookmark must not be empty.":"บุ๊กมาร์กต้องไม่เว้นว่างไว้","Bookmark name cannot contain space characters.":"ชื่อบุ๊กมาร์กต้องไม่มีการเว้นวรรคระหว่างอักขระ","Bookmark name already exists.":"มีชื่อบุ๊กมาร์กนี้อยู่เรียบร้อยแล้ว","bookmark widget":"วิดเจ็ตบุ๊กมาร์ก"},getPluralForm(n){return 0;}}};
e[ 'th' ] ||= { dictionary: {}, getPluralForm: null };
e[ 'th' ].dictionary = Object.assign( e[ 'th' ].dictionary, dictionary );
e[ 'th' ].getPluralForm = getPluralForm;
} )( window.CKEDITOR_TRANSLATIONS ||= {} );
