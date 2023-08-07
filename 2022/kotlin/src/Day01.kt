fun main() {
    fun part1(input: List<String>): Int {
        return input.size
    }

    val input = readInput("input/1")
    println("Size: ${part1(input)}")

    fun day01 (): IntArray {
        val summedArray = ArrayList<Int>()
        var sum = 0
        for (i in input){
            if (i == ""){
                summedArray.add(sum)
                sum = 0
                continue
            }else{
                sum += i.toInt()
            }
        }
        summedArray.sort()
        val topValue = summedArray[summedArray.size -1]
        val topTreeSum = topValue + summedArray[summedArray.size -2] + summedArray[summedArray.size -3]
        return intArrayOf(topValue ,topTreeSum)
    }

    println("Day 1 part 1: ${day01()[0]}")
    println("Day 1 part 2: ${day01()[1]}")

}
