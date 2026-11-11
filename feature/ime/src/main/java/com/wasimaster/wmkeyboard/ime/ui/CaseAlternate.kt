package com.wasimaster.wmkeyboard.ime.ui

import com.wasimaster.wmkeyboard.core.layout.Key
import com.wasimaster.wmkeyboard.core.layout.KeyAction
import com.wasimaster.wmkeyboard.core.script.VERBATIM_DIGITS
import com.wasimaster.wmkeyboard.ime.shiftCased

/**
 * BB-Keyboard: a hold always reaches the *other* case of a letter.
 *
 * The capital a letter's popup offers (issue #108's "Shifted letter on press
 * and hold", or a capital the layout listed itself) is the same letter the key
 * already types once shift is on, so under shift the popup used to offer
 * nothing new. While shift is on, that entry is drawn and typed as the small
 * letter instead, the way the BlackBerry Keyboard lets a hold pick either case.
 *
 * Null when [entry] is not that capital, shift is off, or the key is not a
 * plain single lower-case letter (a key with a shift label of its own already
 * says what shift means for it).
 */
internal fun otherCaseAlternate(key: Key, entry: String, shifted: Boolean): String? {
    if (!shifted || key.action != KeyAction.Text || key.shiftLabel != null) return null
    val base = key.output ?: key.label
    if (base.length != 1 || !base[0].isLowerCase()) return null
    return base.takeIf { entry == base.uppercase() }
}

/** What the popup draws for [entry]: the other case under shift, else the entry cased as usual. */
internal fun shownAlternate(key: Key, entry: String, shifted: Boolean): String =
    otherCaseAlternate(key, entry, shifted) ?: shiftCased(entry, shifted)

/**
 * What picking [entry] types. The small letter goes out marked
 * [VERBATIM_DIGITS], which the service strips and types as given, so the live
 * shift does not turn it straight back into the capital.
 */
internal fun typedAlternate(key: Key, entry: String, shifted: Boolean): String =
    otherCaseAlternate(key, entry, shifted)?.let { VERBATIM_DIGITS + it } ?: entry
