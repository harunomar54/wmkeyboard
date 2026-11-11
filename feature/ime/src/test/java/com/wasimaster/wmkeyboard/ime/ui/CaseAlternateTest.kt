package com.wasimaster.wmkeyboard.ime.ui

import com.wasimaster.wmkeyboard.core.layout.Key
import com.wasimaster.wmkeyboard.core.layout.KeyAction
import com.wasimaster.wmkeyboard.core.script.VERBATIM_DIGITS
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

/** A hold on a letter reaches the other case, whichever way shift is. */
class CaseAlternateTest {

    private val a = Key(label = "a", longPress = listOf("A"))

    @Test
    fun `without shift the capital is offered and typed as itself`() {
        assertEquals("A", shownAlternate(a, "A", shifted = false))
        assertEquals("A", typedAlternate(a, "A", shifted = false))
    }

    @Test
    fun `under shift the capital entry becomes the small letter`() {
        assertEquals("a", shownAlternate(a, "A", shifted = true))
        assertEquals(VERBATIM_DIGITS + "a", typedAlternate(a, "A", shifted = true))
    }

    @Test
    fun `other entries keep the usual shift casing`() {
        val e = Key(label = "e", longPress = listOf("é", "E"))
        assertEquals("É", shownAlternate(e, "é", shifted = true))
        assertEquals("é", typedAlternate(e, "é", shifted = true))
        assertEquals("e", shownAlternate(e, "E", shifted = true))
    }

    @Test
    fun `keys that are not a plain lower-case letter are left alone`() {
        assertNull(otherCaseAlternate(Key(label = "1", longPress = listOf("!")), "!", shifted = true))
        assertNull(otherCaseAlternate(Key(label = "a", shiftLabel = "@", longPress = listOf("A")), "A", shifted = true))
        assertNull(otherCaseAlternate(Key(label = "?123", action = KeyAction.Symbols), "?123", shifted = true))
        assertNull(otherCaseAlternate(Key(label = "A", longPress = listOf("A")), "A", shifted = true))
    }
}
