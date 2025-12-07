use anyhow::{anyhow, Result};
use itertools::Itertools;
use std::iter::repeat_n;

fn splitters(text: String) -> Result<usize> {
    let mut lines = text.lines();
    let first_line = lines.next().ok_or(anyhow!("Invalid input"))?;
    let mut beams = repeat_n(false, first_line.len()).collect_vec();

    let first_beam_position = first_line.find("S").ok_or(anyhow!("Invalid input"))?;
    beams[first_beam_position] = true;

    lines.next();

    let mut count = 0;

    for line in lines.step_by(2) {
        for (splitter_position, _) in line.char_indices().filter(|(_, char)| *char == '^') {
            if beams[splitter_position] {
                beams[splitter_position - 1] = true;
                beams[splitter_position + 1] = true;
                beams[splitter_position] = false;
                count += 1;
            }
        }
    }

    Ok(count)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day07_test.txt")?;
        assert_eq!(splitters(input)?, 21);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day07.txt")?;
        assert_eq!(splitters(input)?, 1590);

        Ok(())
    }
}
