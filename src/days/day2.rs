use itertools::Itertools;

fn parse_levels(text: &str) -> impl Iterator<Item = i32> + '_ {
    text.split_whitespace()
        .filter_map(|x| x.parse::<i32>().ok())
}

fn check_if_report_safe(levels: impl Iterator<Item = i32>) -> bool {
    let mut levels_window = levels.tuple_windows::<(_, _)>().peekable();

    let (first, second) = levels_window.peek().unwrap();
    let diff = first - second;
    let is_increasing = diff > 0;

    levels_window.all(|(a, b)| {
        let diff = a - b;
        let is_trend_consistent = if is_increasing { diff > 0 } else { diff < 0 };
        let is_difference_within_range = (1..=3).contains(&a.abs_diff(b));

        is_trend_consistent && is_difference_within_range
    })
}

fn calc_safe_reports(text: String) -> usize {
    text.lines()
        .filter(|report| check_if_report_safe(parse_levels(report)))
        .count()
}

fn calc_safe_reports_with_one_error(text: String) -> usize {
    text.lines()
        .filter(|report| {
            let levels = parse_levels(report).collect_vec();

            (0..=levels.len()).any(|index| {
                check_if_report_safe(
                    levels
                        .iter()
                        .enumerate()
                        .filter(|(i, _)| index != *i)
                        .map(|(_, x)| *x),
                )
            })
        })
        .count()
}

#[cfg(test)]
mod tests {
    use super::*;
    use anyhow::Result;
    use std::fs;

    #[test]
    fn part1_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day2_test.txt")?;
        assert_eq!(calc_safe_reports(input), 2);

        Ok(())
    }

    #[test]
    fn part1() -> Result<()> {
        let input = fs::read_to_string("inputs/day2.txt")?;
        assert_eq!(calc_safe_reports(input), 379);

        Ok(())
    }

    #[test]
    fn part2_test() -> Result<()> {
        let input = fs::read_to_string("inputs/day2_test.txt")?;
        assert_eq!(calc_safe_reports_with_one_error(input), 4);

        Ok(())
    }

    #[test]
    fn part2() -> Result<()> {
        let input = fs::read_to_string("inputs/day2.txt")?;
        assert_eq!(calc_safe_reports_with_one_error(input), 430);

        Ok(())
    }
}
