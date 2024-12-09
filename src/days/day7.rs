use anyhow::Result;
use itertools::{repeat_n, Itertools};

type Equation = (u64, Vec<u64>);

fn parse_input(input: String) -> Result<Vec<Equation>> {
    let equations = input
        .lines()
        .filter_map(|line| {
            let (str_result, str_numbers) = line.split_once(": ")?;
            let result = str_result.parse().ok()?;
            let numbers = str_numbers
                .split_whitespace()
                .filter_map(|n| n.parse().ok())
                .collect();

            Some((result, numbers))
        })
        .collect();

    Ok(equations)
}

fn apply_operator(operator: &str, a: u64, b: u64) -> u64 {
    match operator {
        "*" => a * b,
        "+" => a + b,
        "||" => (a.to_string() + &b.to_string()).parse().unwrap(),
        _ => a,
    }
}

fn calc_total_calibration_result(equations: Vec<Equation>, operators: &[&str]) -> Result<u64> {
    let total = equations
        .iter()
        .filter(|(result, numbers)| {
            let mut operators_combinations =
                repeat_n(operators.iter(), numbers.len() - 1).multi_cartesian_product();

            operators_combinations.any(|operators| {
                let mut operators_iter = operators.iter();
                let calculated_result =
                    numbers
                        .iter()
                        .copied()
                        .reduce(|current_result, next_number| {
                            apply_operator(
                                operators_iter.next().unwrap_or(&&"+"),
                                current_result,
                                next_number,
                            )
                        });

                match calculated_result {
                    Some(calculated_result) => calculated_result == *result,
                    None => false,
                }
            })
        })
        .map(|(a, _)| a)
        .sum();

    Ok(total)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day7_test.txt")?;
        let equations = parse_input(input)?;
        assert_eq!(calc_total_calibration_result(equations, &["*", "+"])?, 3749);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day7.txt")?;
        let equations = parse_input(input)?;
        assert_eq!(
            calc_total_calibration_result(equations, &["*", "+"])?,
            5030892084481
        );

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day7_test.txt")?;
        let equations = parse_input(input)?;
        assert_eq!(
            calc_total_calibration_result(equations, &["*", "+", "||"])?,
            11387
        );

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day7.txt")?;
        let equations = parse_input(input)?;
        assert_eq!(
            calc_total_calibration_result(equations, &["*", "+", "||"])?,
            91377448644679
        );

        Ok(())
    }
}
