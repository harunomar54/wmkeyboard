package com.wasimaster.wmkeyboard.ime

import com.wasimaster.wmkeyboard.core.gesture.GesturePoint
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test

class BerrySwipeTest {

    private val keyW = 100f
    private val keyH = 140f

    /** A straight stroke from (x0, y0) to (x1, y1) over [ms], sampled in ten steps. */
    private fun line(x0: Float, y0: Float, x1: Float, y1: Float, ms: Long): List<GesturePoint> =
        (0..10).map { i ->
            val f = i / 10f
            GesturePoint(x0 + (x1 - x0) * f, y0 + (y1 - y0) * f, (ms * f).toLong())
        }

    @Test
    fun `a quick straight swipe left deletes a word`() {
        assertEquals(BerrySwipe.DELETE_WORD, berrySwipe(line(800f, 200f, 300f, 230f, 180), keyW, keyH))
    }

    @Test
    fun `a quick swipe down opens the symbols`() {
        assertEquals(BerrySwipe.SYMBOLS, berrySwipe(line(500f, 100f, 520f, 300f, 160), keyW, keyH))
    }

    @Test
    fun `a short left drag is a tap or a two-letter glide`() {
        assertNull(berrySwipe(line(500f, 200f, 350f, 200f, 120), keyW, keyH))
    }

    @Test
    fun `a slow stroke is a glide being traced`() {
        assertNull(berrySwipe(line(800f, 200f, 300f, 200f, 600), keyW, keyH))
    }

    @Test
    fun `a winding stroke is a glide`() {
        val zigzag = listOf(
            GesturePoint(800f, 200f, 0), GesturePoint(650f, 60f, 50), GesturePoint(500f, 340f, 100),
            GesturePoint(400f, 60f, 150), GesturePoint(300f, 200f, 200),
        )
        assertNull(berrySwipe(zigzag, keyW, keyH))
    }

    @Test
    fun `right and up are left to glide and the words on the keys`() {
        assertNull(berrySwipe(line(200f, 200f, 800f, 200f, 150), keyW, keyH))
        assertNull(berrySwipe(line(500f, 400f, 500f, 100f, 150), keyW, keyH))
    }

    @Test
    fun `a diagonal is neither`() {
        assertNull(berrySwipe(line(800f, 100f, 500f, 400f, 150), keyW, keyH))
    }
}
