pub fn part_one(input: &str) -> Option<u32> {
    let mut my_score = 0;

    for line in input.lines() {
        let char_arr : Vec<char> = line.chars().collect();
        my_score += move_score(char_arr[2])?;
        my_score += match_score(char_arr[0],char_arr[2])?;
    }
    Some(my_score)
}

pub fn part_two(input: &str) -> Option<u32> {
    let mut my_score :u32 = 0;

    for line in input.lines() {
        let mut char_arr :Vec<char> = line.chars().collect();
        char_arr.push( match_prediction_calculator(char_arr[2], char_arr[0])?);
        my_score += move_score(char_arr[3])?;
        my_score += match_score(char_arr[0], char_arr[3])?;

    }
    Some(my_score)
}

fn match_prediction_calculator(pred:char, elf_move:char) -> Option<char> {
    match pred {
        'X' => match elf_move {
            'A' => Some('Z'),
            'B' => Some('X'),
            'C' => Some('Y'),
            _ => None,
        },
        'Y' => match elf_move {
            'A' => Some('X'),
            'B' => Some('Y'),
            'C' => Some('Z'),
            _ => None,
        },
        'Z' => match elf_move {
            'A' => Some('Y'),
            'B' => Some('Z'),
            'C' => Some('X'),
            _ => None,
        },
        _ => None
    }


}

fn move_score(letter: char) -> Option<u32>{
    match  letter {
        'X' => Some(1),
        'Y' => Some(2),
        'Z' => Some(3),
        _ => Some(0),
    }
}

fn match_score(p_1_move: char, p_2_move: char) -> Option<u32>{
    match p_1_move {
        'A' => match p_2_move {
            'X' => Some(3),
            'Y' => Some(6),
            'Z' => Some(0),
            _ => None
        },
        'B' => match p_2_move {
            'X' => Some(0),
            'Y' => Some(3),
            'Z' => Some(6),
            _ => None
        },
        'C' => match p_2_move {
            'X' => Some(6),
            'Y' => Some(0),
            'Z' => Some(3),
            _ => None
        },
        _ => None

    }
}

fn main() {
    let input = &advent_of_code::read_file("inputs", 2);
    advent_of_code::solve!(1, part_one, input);
    advent_of_code::solve!(2, part_two, input);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_part_one() {
        let input = advent_of_code::read_file("examples", 2);
        assert_eq!(part_one(&input), None);
    }

    #[test]
    fn test_part_two() {
        let input = advent_of_code::read_file("examples", 2);
        assert_eq!(part_two(&input), None);
    }
}
