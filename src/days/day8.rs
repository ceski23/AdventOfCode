use anyhow::Result;
use itertools::Itertools;
use ndarray::Array2;

fn parse_input(input: String) -> Result<Array2<String>> {
    let size = input.lines().count();
    let x = input
        .lines()
        .flat_map(|line| line.chars().map(|c| c.to_string()).collect_vec())
        .collect_vec();

    Ok(Array2::from_shape_vec((size, size), x)?)
}

fn convert_position_to_coordinates(position: usize, size: usize) -> (usize, usize) {
    (position / size, position % size)
}

fn calc_line(p1: (i32, i32), p2: (i32, i32)) -> (i32, i32) {
    let a = (p2.0 - p1.0) / (p2.1 - p1.1);
    let b = p1.0 - a * p1.1;

    (a, b)
}

fn find_antennas(map: Array2<String>, frequency: &str) -> Result<()> {
    let positions = map
        .iter()
        .positions(|c| c == frequency)
        .map(|pos| convert_position_to_coordinates(pos, map.ncols()))
        .permutations(2)
        .map(|v| {
            calc_line(
                (v[0].0 as i32, v[0].1 as i32),
                (v[1].0 as i32, v[1].1 as i32),
            )
        });

    println!("{:?}", positions.collect_vec());

    Ok(())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day8_test.txt")?;
        let map = parse_input(input)?;
        // assert_eq!(count_visited_positions(map)?, 41);
        find_antennas(map, "a")?;

        Ok(())
    }

    // #[test]
    // fn part1() -> Result<()> {
    //     let input = fs::read_to_string("inputs/day6.txt")?;
    //     let map = parse_input(input)?;
    //     assert_eq!(count_visited_positions(map)?, 4665);

    //     Ok(())
    // }
}
