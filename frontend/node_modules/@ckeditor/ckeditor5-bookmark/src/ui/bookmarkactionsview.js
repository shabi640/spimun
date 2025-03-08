/**
 * @license Copyright (c) 2003-2025, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-licensing-options
 */
/**
 * @module bookmark/ui/bookmarkactionsview
 */
import { LabelView, ButtonView, View, ViewCollection, FocusCycler } from 'ckeditor5/src/ui.js';
import { FocusTracker, KeystrokeHandler } from 'ckeditor5/src/utils.js';
import { icons } from 'ckeditor5/src/core.js';
// eslint-disable-next-line ckeditor5-rules/ckeditor-imports
import '@ckeditor/ckeditor5-ui/theme/components/responsive-form/responsiveform.css';
import '../../theme/bookmarkactions.css';
/**
 * The bookmark actions view class. This view displays the bookmark preview, allows
 * removing or editing the bookmark.
 */
export default class BookmarkActionsView extends View {
    /**
     * @inheritDoc
     */
    constructor(locale) {
        super(locale);
        /**
         * Tracks information about DOM focus in the actions.
         */
        this.focusTracker = new FocusTracker();
        /**
         * An instance of the {@link module:utils/keystrokehandler~KeystrokeHandler}.
         */
        this.keystrokes = new KeystrokeHandler();
        /**
         * A collection of views that can be focused in the view.
         */
        this._focusables = new ViewCollection();
        const t = locale.t;
        this.bookmarkPreviewView = this._createBookmarkPreviewView();
        this.removeButtonView = this._createButton(t('Remove bookmark'), icons.remove, 'remove', this.bookmarkPreviewView);
        this.editButtonView = this._createButton(t('Edit bookmark'), icons.pencil, 'edit', this.bookmarkPreviewView);
        this.set('id', undefined);
        this._focusCycler = new FocusCycler({
            focusables: this._focusables,
            focusTracker: this.focusTracker,
            keystrokeHandler: this.keystrokes,
            actions: {
                // Navigate fields backwards using the Shift + Tab keystroke.
                focusPrevious: 'shift + tab',
                // Navigate fields forwards using the Tab key.
                focusNext: 'tab'
            }
        });
        this.setTemplate({
            tag: 'div',
            attributes: {
                class: [
                    'ck',
                    'ck-bookmark-actions',
                    'ck-responsive-form'
                ],
                // https://github.com/ckeditor/ckeditor5-link/issues/90
                tabindex: '-1'
            },
            children: [
                this.bookmarkPreviewView,
                this.editButtonView,
                this.removeButtonView
            ]
        });
    }
    /**
     * @inheritDoc
     */
    render() {
        super.render();
        const childViews = [
            this.editButtonView,
            this.removeButtonView
        ];
        childViews.forEach(v => {
            // Register the view as focusable.
            this._focusables.add(v);
            // Register the view in the focus tracker.
            this.focusTracker.add(v.element);
        });
        // Start listening for the keystrokes coming from #element.
        this.keystrokes.listenTo(this.element);
    }
    /**
     * @inheritDoc
     */
    destroy() {
        super.destroy();
        this.focusTracker.destroy();
        this.keystrokes.destroy();
    }
    /**
     * Focuses the fist {@link #_focusables} in the actions.
     */
    focus() {
        this._focusCycler.focusFirst();
    }
    /**
     * Creates a button view.
     *
     * @param label The button label.
     * @param icon The button icon.
     * @param eventName An event name that the `ButtonView#execute` event will be delegated to.
     * @param additionalLabel An additional label outside the button.
     * @returns The button view instance.
     */
    _createButton(label, icon, eventName, additionalLabel) {
        const button = new ButtonView(this.locale);
        button.set({
            label,
            icon,
            tooltip: true
        });
        button.delegate('execute').to(this, eventName);
        // Since button label `id` is bound to the `ariaLabelledBy` property
        // we need to modify this binding to include only the first ID token
        // as this button will be labeled by multiple labels.
        button.labelView.unbind('id');
        button.labelView.bind('id').to(button, 'ariaLabelledBy', ariaLabelledBy => {
            return getFirstToken(ariaLabelledBy);
        });
        button.ariaLabelledBy = `${button.ariaLabelledBy} ${additionalLabel.id}`;
        return button;
    }
    /**
     * Creates a bookmark name preview label.
     *
     * @returns The label view instance.
     */
    _createBookmarkPreviewView() {
        const label = new LabelView(this.locale);
        label.extendTemplate({
            attributes: {
                class: [
                    'ck',
                    'ck-bookmark-actions__preview'
                ]
            }
        });
        // Bind label text with the bookmark ID.
        label.bind('text').to(this, 'id');
        return label;
    }
}
/**
 * Returns the first token from space separated token list.
 */
function getFirstToken(tokenList) {
    return tokenList.split(' ')[0];
}
