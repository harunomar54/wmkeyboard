package com.wasimaster.wmkeyboard.ime

import com.wasimaster.wmkeyboard.core.gesture.GesturePoint
import kotlin.math.abs
import kotlin.math.hypot

/** What a BlackBerry-style swipe over the keys asks for. */
internal enum class BerrySwipe {
    /** A swipe left: delete the word behind the caret. */
    DELETE_WORD,

    /** A swipe down: open the symbols, or turn their page when they are up. */
    SYMBOLS,
}

/**
 * Reads a finished stroke as one of the BlackBerry Keyboard's board swipes, or
 * null when it is anything else (a tap, a glide, a flick up for a word).
 *
 * Judged at the lift, never on the way: a glide that sets off left or down
 * looks like a swipe for its first few millimetres, so only the whole stroke
 * can say. A swipe has to be all three of
 * - long: left across at least [minLeftKeys] key widths, or down across at
 *   least [minDownRows] key heights, so a sloppy tap or a two-letter glide
 *   never qualifies;
 * - straight: the path no more than [maxDetour] times the distance between
 *   its ends, and inside [maxOffAxis] of the axis (sideways drift over travel);
 * - quick: over within [maxDurationMs], since a glide is traced, not thrown.
 *
 * Rightward and upward strokes are never swipes here: right belongs to glide
 * typing and up to the words on the keys.
 */
internal fun berrySwipe(
    points: List<GesturePoint>,
    keyWidthPx: Float,
    keyHeightPx: Float,
    minLeftKeys: Float = BERRY_MIN_LEFT_KEYS,
    minDownRows: Float = BERRY_MIN_DOWN_ROWS,
    maxDetour: Float = BERRY_MAX_DETOUR,
    maxOffAxis: Float = BERRY_MAX_OFF_AXIS,
    maxDurationMs: Long = BERRY_MAX_DURATION_MS,
): BerrySwipe? {
    if (points.size < 2 || keyWidthPx <= 0f || keyHeightPx <= 0f) return null
    val first = points.first()
    val last = points.last()
    val duration = last.t - first.t
    if (duration < 0 || duration > maxDurationMs) return null
    val dx = last.x - first.x
    val dy = last.y - first.y
    val chord = hypot(dx, dy)
    if (chord <= 0f) return null
    var path = 0f
    for (i in 1 until points.size) {
        path += hypot(points[i].x - points[i - 1].x, points[i].y - points[i - 1].y)
    }
    if (path > chord * maxDetour) return null
    return when {
        dx <= -minLeftKeys * keyWidthPx && abs(dy) <= abs(dx) * maxOffAxis -> BerrySwipe.DELETE_WORD
        dy >= minDownRows * keyHeightPx && abs(dx) <= abs(dy) * maxOffAxis -> BerrySwipe.SYMBOLS
        else -> null
    }
}

/** A left swipe crosses at least this many key widths (about a fifth of the board). */
internal const val BERRY_MIN_LEFT_KEYS = 2.2f

/** A down swipe covers at least this many key heights. */
internal const val BERRY_MIN_DOWN_ROWS = 1.1f

/** Path length over end-to-end distance; a straight line is 1. */
internal const val BERRY_MAX_DETOUR = 1.2f

/** Sideways drift per unit of travel: 0.45 is about 24° off the axis. */
internal const val BERRY_MAX_OFF_AXIS = 0.45f

/** A swipe is thrown; anything slower is a glide being traced. */
internal const val BERRY_MAX_DURATION_MS = 350L
