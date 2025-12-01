use anyhow::{Ok, Result};
use itertools::Itertools;
use ndarray::{s, Array, Array2, ArrayBase, ArrayView, Axis, Dim, Ix2, RawData, Slice};

fn check_slice(slice: &Slice) -> bool {
    false
}

fn rot90<S>(arr: &mut ArrayBase<S, Ix2>)
where
    S: RawData,
{
    arr.swap_axes(0, 1);
    arr.invert_axis(Axis(0));
}

fn find_horizontally(
    array: &Array2<String>,
    word: &str,
    (pos_y, pos_x): (usize, usize),
) -> Option<()> {
    if pos_x + word.len() > array.shape()[1] {
        return None;
    }

    let found_word = &array
        .slice(s![pos_y, pos_x..pos_x + word.len()])
        .iter()
        .join("");

    (found_word == word).then_some(())
}

fn find_horizontally_rev(
    array: &Array2<String>,
    word: &str,
    (pos_y, pos_x): (usize, usize),
) -> Option<()> {
    if pos_x < word.len() - 1 {
        return None;
    }

    let found_word = &array
        .slice(s![pos_y, pos_x + 1 - word.len()..pos_x + 1])
        .iter()
        .rev()
        .join("");

    (found_word == word).then_some(())
}

fn find_vertically(
    array: &Array2<String>,
    word: &str,
    (pos_y, pos_x): (usize, usize),
) -> Option<()> {
    if pos_y + word.len() > array.shape()[0] {
        return None;
    }

    let found_word = &array
        .slice(s![pos_y..pos_y + word.len(), pos_x])
        .iter()
        .join("");

    (found_word == word).then_some(())
}

fn find_vertically_rev(
    array: &Array2<String>,
    word: &str,
    (pos_y, pos_x): (usize, usize),
) -> Option<()> {
    if pos_y < word.len() - 1 {
        return None;
    }

    let found_word = &array
        .slice(s![pos_y + 1 - word.len()..pos_y + 1, pos_x])
        .iter()
        .rev()
        .join("");

    (found_word == word).then_some(())
}

fn find_diag_right(
    array: &Array2<String>,
    word: &str,
    (pos_y, pos_x): (usize, usize),
) -> Option<()> {
    let shape = array.shape();

    if (pos_y + word.len() - 1) >= shape[0] || (pos_x + word.len() - 1) >= shape[1] {
        return None;
    }

    let found_word = &array
        .slice(s![pos_y..pos_y + word.len(), pos_x..pos_x + word.len()])
        .diag()
        .iter()
        .join("");

    (found_word == word).then_some(())
}

fn find_diag_right_rev(
    array: &Array2<String>,
    word: &str,
    (pos_y, pos_x): (usize, usize),
) -> Option<()> {
    if pos_y < word.len() - 1 || pos_x < word.len() - 1 {
        return None;
    }

    let found_word = &array
        .slice(s![
            pos_y + 1 - word.len()..pos_y + 1,
            pos_x + 1 - word.len()..pos_x + 1
        ])
        .diag()
        .iter()
        .rev()
        .join("");

    (found_word == word).then_some(())
}

fn find_diag_left(
    array: &Array2<String>,
    word: &str,
    (pos_y, pos_x): (usize, usize),
) -> Option<()> {
    let shape = array.shape();

    if (pos_y + word.len()) > shape[0] || pos_x < (word.len() - 1) || pos_x >= array.ncols() {
        return None;
    }

    let found_word = &array
        .slice(s![
            pos_y..pos_y + word.len(),
            pos_x + 1 - word.len()..pos_x + 1
        ])
        .slice(s![..; -1, ..; 1])
        .diag()
        .iter()
        .rev()
        .join("");

    (found_word == word).then_some(())
}

fn find_diag_left_rev(
    array: &Array2<String>,
    word: &str,
    (pos_y, pos_x): (usize, usize),
) -> Option<()> {
    if pos_y < word.len() - 1 || pos_x + word.len() > array.shape()[1] {
        return None;
    }

    let found_word = &array
        .slice(s![
            pos_y + 1 - word.len()..pos_y + 1,
            pos_x..pos_x + word.len()
        ])
        .slice(s![..; -1, ..; 1])
        .diag()
        .iter()
        .join("");

    (found_word == word).then_some(())
}

fn parse_input(input: String) -> Result<Array2<String>> {
    let mut size = 0;
    let x = input
        .lines()
        .flat_map(|line| {
            size = line.len();
            line.chars().map(|c| c.to_string()).collect_vec()
        })
        .collect_vec();

    Ok(Array2::from_shape_vec((size, size), x)?)
}

fn run(input: String) -> Result<usize> {
    let array = parse_input(input)?;
    let count = array
        .indexed_iter()
        .filter(|(_, value)| *value == "X")
        .map(|(position, _)| {
            [
                find_horizontally(&array, "XMAS", position),
                find_horizontally_rev(&array, "XMAS", position),
                find_vertically(&array, "XMAS", position),
                find_vertically_rev(&array, "XMAS", position),
                find_diag_right(&array, "XMAS", position),
                find_diag_right_rev(&array, "XMAS", position),
                find_diag_left(&array, "XMAS", position),
                find_diag_left_rev(&array, "XMAS", position),
            ]
            .iter()
            .filter_map(|x| *x)
            .count()
        })
        .sum();

    Ok(count)
}

fn run2(input: String) -> Result<usize> {
    let array = parse_input(input)?;
    let count = array
        .indexed_iter()
        .filter(|(_, value)| *value == "M")
        .map(|(position, _)| {
            let mut c = 0;
            for i in 0..=3 {
                let mut view = array.clone();
                for _ in 0..i {
                    view.swap_axes(0, 1);
                    view.invert_axis(Axis(0));
                }
                let diag_right = find_diag_right(&view, "MAS", position);
                let diag_left = find_diag_left(&view, "MAS", (position.0, position.1 + 2));

                if diag_right.and(diag_left).is_some() {
                    c += 1;
                }
            }

            // let x = [].iter().filter_map(|x| *x).count();
            // println!("{:?}: {:?}", position, x);
            // println!("diag_right: {:?}", diag_right);
            // println!("diag_left: {:?}", diag_left);

            c
        })
        .sum();

    Ok(count)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day4_test.txt")?;
        assert_eq!(run(input)?, 18);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day4.txt")?;
        assert_eq!(run(input)?, 2644);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day4_test.txt")?;
        // assert_eq!(run2(input)?, 9);
        println!("{:?}", run2(input)?);

        Ok(())
    }

    // #[test]
    // fn part2() -> Result<()> {
    //     let input = fs::read_to_string("inputs/day3.txt")?;
    //     assert_eq!(
    //         sum_uncorrupted_instructions_conditionally(input)?,
    //         100450138
    //     );

    //     Ok(())
    // }
}
