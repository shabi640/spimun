/**
 * @license Copyright (c) 2003-2025, CKSource Holding sp. z o.o. All rights reserved.
 * For licensing, see LICENSE.md or https://ckeditor.com/legal/ckeditor-licensing-options
 */
/**
 * @module bookmark/bookmarkui
 */
import { Plugin } from 'ckeditor5/src/core.js';
import { ContextualBalloon, type ViewWithCssTransitionDisabler } from 'ckeditor5/src/ui.js';
import BookmarkFormView from './ui/bookmarkformview.js';
import BookmarkActionsView from './ui/bookmarkactionsview.js';
import BookmarkEditing from './bookmarkediting.js';
/**
 * The UI plugin of the bookmark feature.
 *
 * It registers the `'bookmark'` UI button in the editor's {@link module:ui/componentfactory~ComponentFactory component factory}
 * which inserts the `bookmark` element upon selection.
 */
export default class BookmarkUI extends Plugin {
    /**
     * The actions view displayed inside of the balloon.
     */
    actionsView: BookmarkActionsView | null;
    /**
     * The form view displayed inside the balloon.
     */
    formView: BookmarkFormView & ViewWithCssTransitionDisabler | null;
    /**
     * The contextual balloon plugin instance.
     */
    private _balloon;
    /**
     * @inheritDoc
     */
    static get requires(): readonly [typeof BookmarkEditing, typeof ContextualBalloon];
    /**
     * @inheritDoc
     */
    static get pluginName(): "BookmarkUI";
    /**
     * @inheritDoc
     */
    static get isOfficialPlugin(): true;
    /**
     * @inheritDoc
     */
    init(): void;
    /**
     * @inheritDoc
     */
    destroy(): void;
    /**
     * Creates views.
     */
    private _createViews;
    /**
     * Creates the {@link module:bookmark/ui/bookmarkactionsview~BookmarkActionsView} instance.
     */
    private _createActionsView;
    /**
     * Creates the {@link module:bookmark/ui/bookmarkformview~BookmarkFormView} instance.
     */
    private _createFormView;
    /**
     * Creates a toolbar Bookmark button. Clicking this button will show
     * a {@link #_balloon} attached to the selection.
     */
    private _createToolbarBookmarkButton;
    /**
     * Creates a button for `bookmark` command to use either in toolbar or in menu bar.
     */
    private _createButton;
    /**
     * Attaches actions that control whether the balloon panel containing the
     * {@link #formView} should be displayed.
     */
    private _enableBalloonActivators;
    /**
     * Attaches actions that control whether the balloon panel containing the
     * {@link #formView} is visible or not.
     */
    private _enableUserBalloonInteractions;
    /**
     * Updates the button label. If bookmark is selected label is set to 'Update' otherwise
     * it is 'Insert'.
     */
    private _updateFormButtonLabel;
    /**
     * Adds the {@link #actionsView} to the {@link #_balloon}.
     *
     * @internal
     */
    _addActionsView(): void;
    /**
     * Adds the {@link #formView} to the {@link #_balloon}.
     */
    private _addFormView;
    /**
     * Closes the form view. Decides whether the balloon should be hidden completely.
     */
    private _closeFormView;
    /**
     * Removes the {@link #formView} from the {@link #_balloon}.
     */
    private _removeFormView;
    /**
     * Shows the correct UI type. It is either {@link #formView} or {@link #actionsView}.
     */
    private _showUI;
    /**
     * Removes the {@link #formView} from the {@link #_balloon}.
     *
     * See {@link #_addFormView}, {@link #_addActionsView}.
     */
    private _hideUI;
    /**
     * Makes the UI react to the {@link module:ui/editorui/editorui~EditorUI#event:update} event to
     * reposition itself when the editor UI should be refreshed.
     *
     * See: {@link #_hideUI} to learn when the UI stops reacting to the `update` event.
     */
    private _startUpdatingUI;
    /**
     * Returns `true` when {@link #formView} is in the {@link #_balloon}.
     */
    private get _isFormInPanel();
    /**
     * Returns `true` when {@link #actionsView} is in the {@link #_balloon}.
     */
    private get _areActionsInPanel();
    /**
     * Returns `true` when {@link #actionsView} is in the {@link #_balloon} and it is
     * currently visible.
     */
    private get _areActionsVisible();
    /**
     * Returns `true` when {@link #actionsView} or {@link #formView} is in the {@link #_balloon}.
     */
    private get _isUIInPanel();
    /**
     * Returns `true` when {@link #actionsView} or {@link #formView} is in the {@link #_balloon} and it is
     * currently visible.
     */
    private get _isUIVisible();
    /**
     * Returns positioning options for the {@link #_balloon}. They control the way the balloon is attached
     * to the target element or selection.
     */
    private _getBalloonPositionData;
    /**
     * Returns the bookmark {@link module:engine/view/attributeelement~AttributeElement} under
     * the {@link module:engine/view/document~Document editing view's} selection or `null`
     * if there is none.
     */
    private _getSelectedBookmarkElement;
    /**
     * Displays a fake visual selection when the contextual balloon is displayed.
     *
     * This adds a 'bookmark-ui' marker into the document that is rendered as a highlight on selected text fragment.
     */
    private _showFakeVisualSelection;
    /**
     * Hides the fake visual selection created in {@link #_showFakeVisualSelection}.
     */
    private _hideFakeVisualSelection;
}
