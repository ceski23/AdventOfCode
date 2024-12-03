use anyhow::Result;
use regex::Regex;

fn calc_instructions(text: String) -> Result<u32> {
    let real_mul_pattern = Regex::new(r"mul\((\d{1,3}),(\d{1,3})\)")?;
    let sum = real_mul_pattern
        .captures_iter(&text)
        .filter_map(|capture| {
            let (_, [a, b]) = capture.extract();

            Some((a.parse::<u32>().ok()?, b.parse::<u32>().ok()?))
        })
        .map(|(a, b)| a * b)
        .sum::<u32>();

    Ok(sum)
}

fn calc_instructions_conditionally(text: String) -> Result<u32> {
    let real_mul_pattern = Regex::new(r"(?:mul\((\d{1,3}),(\d{1,3})\))|(do\(\))|(don't\(\))")?;
    let sum = real_mul_pattern
        .captures_iter(&text)
        .fold((true, 0), |(should_parse, sum), capture| {
            if capture.get(3).is_some() {
                return (true, sum);
            }

            if capture.get(4).is_some() {
                return (false, sum);
            }

            if should_parse {
                let n1 = capture
                    .get(1)
                    .unwrap()
                    .as_str()
                    .parse::<u32>()
                    .unwrap_or_default();
                let n2 = capture
                    .get(2)
                    .unwrap()
                    .as_str()
                    .parse::<u32>()
                    .unwrap_or_default();

                return (should_parse, sum + (n1 * n2));
            }

            (should_parse, sum)
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
        assert_eq!(calc_instructions(input)?, 161);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day3.txt")?;
        assert_eq!(calc_instructions(input)?, 173517243);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day3_test2.txt")?;
        assert_eq!(calc_instructions_conditionally(input)?, 48);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day3.txt")?;
        assert_eq!(calc_instructions_conditionally(input)?, 100450138);

        Ok(())
    }
}
