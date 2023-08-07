
/**
 * @author  LUCAS LARSSON
 * @created 2023-06-26
 */
fun main(){
    val input = readInput("input/2")

    val charMapper = mapOf('A' to 1, 'B' to 2, 'C' to 3, 'X' to 1, 'Y' to 2, 'Z' to 3)

    fun myWinScore(elf: Char, mine: Char): Int {
        return when {
            (elf == 'A' && mine == 'Z') || (elf == 'B' && mine == 'X') || (elf == 'C' && mine == 'Y') -> 0
            (elf == 'A' && mine == 'Y') || (elf == 'B' && mine == 'Z') || (elf == 'C' && mine == 'X') -> 6
            else -> 3
        }
    }

    fun selector(elf: Char, mine: Char): Int {
        return when(mine){
            'X' -> when(elf){
                'A' -> 3    // 3 + 0
                'B' -> 1    // 1 + 0
                else -> 2   // 2 + 0
            }
            'Y' -> when(elf){
                'A' -> 4    // 1 + 3
                'B' -> 5    // 2 + 3
                else -> 6   // 3 + 3
            }
            else -> when(elf){
                'A' -> 8    // 2 + 6
                'B' -> 9    // 3 + 6
                else -> 7   // 1 + 6
            }
        }
    }

    fun part1(input: List<String>): Int {
        return input.parallelStream().mapToInt { i ->
            charMapper[i[2]]!! + myWinScore(i[0], i[2])
        }.sum()
    }

    fun part2(input: List<String>):Int {
        return input.map { i -> selector(i[0], i[2])}.sum()
    }

    println("Part1 : ${part1(input)}") // 13268
    println("Part2 : ${part2(input)}") // 15508
}