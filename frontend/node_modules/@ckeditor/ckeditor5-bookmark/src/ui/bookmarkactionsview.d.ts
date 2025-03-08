/**
 * @license Copyright (c) 2003-2025, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-licensing-options
 */
/**
 * @module bookmark/ui/bookmarkactionsview
 */
import { LabelView, ButtonView, View } from 'ckeditor5/src/ui.js';
import { FocusTracker, KeystrokeHandler, type LocaleTranslate, type Locale } from 'ckeditor5/src/utils.js';
import '@ckeditor/ckeditor5-ui/theme/components/responsive-form/responsiveform.css';
import '../../theme/bookmarkactions.css';
/**
 * The bookmark actions view class. This view displays the bookmark preview, allows
 * removing or editing the bookmark.
 */
export default class BookmarkActionsView extends View {
    /**
     * Tracks information about DOM focus in the actions.
     */
    readonly focusTracker: FocusTracker;
    /**
     * An instance of the {@link module:utils/keystrokehandler~KeystrokeHandler}.
     */
    readonly keystrokes: KeystrokeHandler;
    /**
     * The bookmark preview view.
     */
    bookmarkPreviewView: LabelView;
    /**
     * The remove button view.
     */
    removeButtonView: ButtonView;
    /**
     * The edit bookmark button view.
     */
    editButtonView: ButtonView;
    /**
     * The id preview view.
     *
     * @observable
     */
    id: string | undefined;
    /**
     * A collection of views that can be focused in the view.
     */
    private readonly _focusables;
    /**
     * Helps cycling over {@link #_focusables} in the view.
     */
    private readonly _focusCycler;
    t: LocaleTranslate;
    /**
     * @inheritDoc
     */
    constructor(locale: Locale);
    /**
     * @inheritDoc
     */
    render(): void;
    /**
     * @inheritDoc
     */
    destroy(): void;
    /**
     * Focuses the fist {@link #_focusables} in the actions.
     */
    focus(): void;
    /**
     * Creates a button view.
     *
     * @param label The button label.
     * @param icon The button icon.
     * @param eventName An event name that the `ButtonView#execute` event will be delegated to.
     * @param additionalLabel An additional label outside the button.
     * @returns The button view instance.
     */
    private _createButton;
    /**
     * Creates a bookmark name preview label.
     *
     * @returns The label view instance.
     */
    private _createBookmarkPreviewView;
}
/**
 * Fired when the {@link ~BookmarkActionsView#editButtonView} is clicked.
 *
 * @eventName ~BookmarkActionsView#edit
 */
export type EditEvent = {
    name: 'edit';
    args: [];
};
/**
 * Fired when the {@link ~BookmarkActionsView#removeButtonView} is clicked.
 *
 * @eventName ~BookmarkActionsView#remove
 */
export type RemoveEvent = {
    name: 'remove';
    args: [];
};
