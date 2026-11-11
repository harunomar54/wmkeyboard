package com.wasimaster.wmkeyboard.core.dictionaries

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/**
 * BB-Keyboard's name capitals in the shipped English capitals list: names
 * that must be there, and everyday words or misspellings that must never be,
 * since a word on this list is capitalized whenever it is typed in small
 * letters.
 */
class BerryNameCapitalsTest {

    private val spellings: List<String> by lazy {
        val file = listOf(
            File("src/main/assets/dictionaries/en_caps.txt"),
            File("app/src/main/assets/dictionaries/en_caps.txt"),
        ).first { it.exists() }
        file.readLines().map { it.trim() }.filter { it.isNotEmpty() && !it.startsWith("#") }
    }

    @Test
    fun `English and Arabic names are on the list`() {
        val wanted = listOf(
            "John", "Henry", "Billy", "Jayden", "Abdullah", "Abdurahman", "Abdirahman", "Abdulrahman",
            "Bilal", "Musa", "Yusuf", "Zayd", "Layth", "Harun", "Hamza", "Amir", "Khadija", "Hodan",
            "Maxamed", "Mohamed", "Eid", "Ramadan", "Quran", "Mecca",
        )
        val missing = wanted.filterNot { it in spellings }
        assertEquals("missing: $missing", emptyList<String>(), missing)
    }

    @Test
    fun `everyday words and misspellings never are`() {
        val banned = listOf(
            "Will", "Mark", "Grace", "Rose", "May", "Said", "Sad", "Dua", "Iman", "Ameen", "Salam",
            "Jannah", "Ayah", "Fajr", "Abd", "Isa", "Isreal", "Willam", "Teh", "Jhon",
        )
        val present = banned.filter { it in spellings }
        assertEquals("must not capitalize: $present", emptyList<String>(), present)
    }

    @Test
    fun `each spelling is on the list once`() {
        val repeated = spellings.groupBy { it }.filterValues { it.size > 1 }.keys
        assertTrue("listed twice: $repeated", repeated.isEmpty())
    }
}
