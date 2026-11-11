package com.wasimaster.wmkeyboard.ime.ui

import androidx.compose.runtime.Composable
import androidx.compose.runtime.State
import androidx.compose.runtime.derivedStateOf
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.graphics.Color

/**
 * The word a space will put in, for the spacebar to show in place of its
 * label (the BlackBerry Keyboard's habit), or null for the usual label.
 *
 * It is [com.wasimaster.wmkeyboard.ime.KeyboardUiState.autocorrectWord], the
 * promise the strip already colours: set only once autocorrect has decided,
 * so what the spacebar shows is what the space types. Read from the live
 * state through a derived value, so a keystroke recomposes this one label
 * when the answer changes and the key grid not at all.
 */
@Composable
internal fun rememberSpacebarCorrection(): State<String?> {
    val live = LocalLiveUiState.current
    if (live == null || LocalKeyboardPreviewHost.current) return remember { mutableStateOf(null) }
    return remember(live) {
        derivedStateOf {
            val now = live.value
            if (now.settings.layoutBehavior.spacebarCorrection) {
                // A shortcut fires before autocorrect on the same space, so
                // what it expands to is what the space types.
                SpacebarSnippetPreview.text.value
                    ?: now.autocorrectWord?.takeIf { it.isNotBlank() }
            } else {
                null
            }
        }
    }
}

/**
 * What a space would expand the word being typed into, when it is a snippet
 * trigger. The service writes it on every keystroke; null when the word fires
 * nothing. A snapshot state of its own, as the live speed readout is, so the
 * spacebar alone redraws when it changes.
 */
internal object SpacebarSnippetPreview {
    val text = mutableStateOf<String?>(null)
}

/** The BlackBerry Keyboard's green for a correction waiting on the spacebar. */
internal val SpacebarCorrectionGreen = Color(0xFF9DD69D)
