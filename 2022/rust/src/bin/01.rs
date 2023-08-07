pub fn part_one(input: &str) -> Option<u32> {

let mut cal_vector: Vec<u32> = group_and_sum_cal(input);
    cal_vector.sort_by(|a,b|b.cmp(a));

    Some(cal_vector[0])
}



pub fn part_two(input: &str) -> Option<u32> {
    let mut cal_vector: Vec<u32> = group_and_sum_cal(input);
    cal_vector.sort_by(|a,b|b.cmp(a));

    let top_three_cal_sum = cal_vector[0] +cal_vector[1] +cal_vector[2];

    Some(top_three_cal_sum)
}


fn group_and_sum_cal(input: &str)-> Vec<u32>{
    let mut numbers: Vec<u32> = Vec::new();
    let mut sum: u32 = 0;

    for line in input.lines() {
        if line.is_empty(){
            numbers.push(sum);
            sum = 0;
        } else {
            sum += line.trim().parse::<u32>().unwrap();
        }

    }
    return numbers;
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 1);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 1);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 1);
        assert_eq!(part_two(&input), None);
    }
}

