use anyhow::{anyhow, Result};
use itertools::Itertools;

fn parse_input(text: String) -> Result<u64> {
    let lines = text.lines().collect_vec();
    let (operations_line, elements) = lines.split_last().ok_or(anyhow!("Invalid input"))?;
    let operations: Vec<&str> = operations_line.split_whitespace().collect();

    let values: Vec<u64> = elements
        .iter()
        .flat_map(|line| line.split_whitespace())
        .filter_map(|item| item.parse().ok())
        .collect();

    let results: Vec<u64> = operations
        .iter()
        .enumerate()
        .map(|(column, &operation)| {
            let column_values = values.iter().skip(column).step_by(operations.len());
            match operation {
                "*" => column_values.product(),
                "+" => column_values.sum(),
                _ => 0,
            }
        })
        .collect();

    Ok(results.iter().sum())
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day06_test.txt")?;
        let data = parse_input(input)?;
        assert_eq!(data, 4277556);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day06.txt")?;
        let data = parse_input(input)?;
        assert_eq!(data, 5877594983578);

        Ok(())
    }
}
