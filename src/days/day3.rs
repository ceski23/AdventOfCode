use anyhow::Result;
use regex::Regex;

fn sum_uncorrupted_instructions(text: String) -> Result<u32> {
    let instruction_pattern = Regex::new(r"mul\((?<x>\d{1,3}),(?<y>\d{1,3})\)")?;
    let sum = instruction_pattern
        .captures_iter(&text)
        .filter_map(|capture| {
            let x = &capture["x"].parse::<u32>().ok()?;
            let y = &capture["y"].parse::<u32>().ok()?;

            Some(x * y)
        })
        .sum();

    Ok(sum)
}

fn sum_uncorrupted_instructions_conditionally(text: String) -> Result<u32> {
    let instruction_pattern = Regex::new(
        r"(?:mul\((?<x>\d{1,3}),(?<y>\d{1,3})\))|(?<enable>do\(\))|(?<disable>don't\(\))",
    )?;
    let sum = instruction_pattern
        .captures_iter(&text)
        .fold((true, 0), |(should_parse, sum), groups| {
            if groups.name("enable").is_some() {
                return (true, sum);
            }

            if groups.name("disable").is_some() {
                return (false, sum);
            }

            match (should_parse, groups.name("x"), groups.name("y")) {
                (true, Some(x_match), Some(y_match)) => {
                    let x = x_match.as_str().parse::<u32>().unwrap_or_default();
                    let y = y_match.as_str().parse::<u32>().unwrap_or_default();

                    (should_parse, sum + (x * y))
                }
                _ => (should_parse, sum),
            }
        })
        .1;

    Ok(sum)
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day3_test.txt")?;
        assert_eq!(sum_uncorrupted_instructions(input)?, 161);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day3.txt")?;
        assert_eq!(sum_uncorrupted_instructions(input)?, 173517243);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day3_test2.txt")?;
        assert_eq!(sum_uncorrupted_instructions_conditionally(input)?, 48);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day3.txt")?;
        assert_eq!(
            sum_uncorrupted_instructions_conditionally(input)?,
            100450138
        );

        Ok(())
    }
}
