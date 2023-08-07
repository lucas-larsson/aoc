import java.io.File
import java.io.FileOutputStream
import java.math.BigInteger
import java.net.HttpURLConnection
import java.security.MessageDigest
import java.net.URL

/**
 * Reads lines from the given input txt file.
 */
fun readInput(name: String) = File("src", "$name.txt")
    .readLines()

/**
 * Converts string to md5 hash.
 */
fun String.md5() = BigInteger(1, MessageDigest.getInstance("MD5").digest(toByteArray()))
    .toString(16)
    .padStart(32, '0')

/**
 * The cleaner shorthand for printing output.
 */
fun Any?.println() = println(this)

/**
 * downloads file from the given url and saves it to the given path.
 */
fun downloadFile(url: URL, path: String, cookie : String) {
    // commented out code is for debugging and is not needed for the function to work
    val connection: HttpURLConnection = url.openConnection() as HttpURLConnection
//    connection.requestMethod = "GET"
    connection.setRequestProperty("Cookie", "session=$cookie")
    connection.connect()
//    val code = connection.responseCode
//    val message = connection.responseMessage
//    println("Response code: $code")
//    println("Response message: $message")

    val inputStream = connection.inputStream
    inputStream.use { input ->
        val file = File(path)
        file.parentFile.mkdirs()
        file.createNewFile()
        val outputStream = FileOutputStream(file)
        outputStream.use { output ->
            input.copyTo(output)
        }
    }
}

/**
 * downloads all aoc input files to the src folder.
 */
fun downloadAllInputs() {
    for (day in 1..25) {
        val url = URL("https://adventofcode.com/2022/day/$day/input")
        val path = "src/input/$day.txt"
        val sessionCookie = ""  //  <sessionCookie> is your session cookie from the browser
        downloadFile(url, path, sessionCookie)
    }
}