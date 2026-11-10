package com.wasimaster.wmkeyboard.ime.ui

import com.wasimaster.wmkeyboard.core.layout.FlickDirection
import com.wasimaster.wmkeyboard.core.layout.Key
import com.wasimaster.wmkeyboard.core.layout.KeyAction
import com.wasimaster.wmkeyboard.core.layout.KeyAlternate
import com.wasimaster.wmkeyboard.core.settings.TextEditAction
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

/**
 * Which flick keys leave the words on the keys their flick up: a key whose
 * arms all point away from up keeps the word above it reachable, so a
 * BlackBerry-style board (left deletes a word, down opens the symbols) keeps
 * in-letter prediction working.
 */
class OctopusFlickKeysTest {

    private val deleteWord = KeyAlternate(KeyAction.Edit(TextEditAction.DELETE_WORD))
    private val symbols = KeyAlternate(KeyAction.Symbols)

    @Test
    fun `a plain letter never blocks the word`() {
        assertFalse(Key(label = "q").ownsDragFromOctopus())
    }

    @Test
    fun `left and down arms leave the flick up to the word`() {
        val key = Key(
            label = "Q",
            output = "q",
            flickActions = mapOf(FlickDirection.LEFT to deleteWord, FlickDirection.DOWN to symbols),
        )
        assertTrue(key.ownsDrag())
        assertFalse(key.ownsDragFromOctopus())
    }

    @Test
    fun `an upward arm keeps the stroke for the key`() {
        val key = Key(label = "q", flick = mapOf(FlickDirection.UP to "1"))
        assertTrue(key.ownsDragFromOctopus())
    }

    @Test
    fun `an up-right corner arm counts as upward`() {
        val key = Key(label = "q", flick = mapOf(FlickDirection.UP_RIGHT to "1"))
        assertTrue(key.ownsDragFromOctopus())
    }

    @Test
    fun `layer keys still own their drag`() {
        assertTrue(Key(label = "?123", action = KeyAction.Symbols).ownsDragFromOctopus())
    }
}
