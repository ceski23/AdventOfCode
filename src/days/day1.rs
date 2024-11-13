fn read_text(text: String) -> String {
    text
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::error::Error;
    use std::fs;

    #[test]
    fn part1() -> Result<(), Box<dyn Error>> {
        let input = fs::read_to_string("inputs/input.txt")?;
        assert_eq!(read_text(input), "Hello World!");

        Ok(())
    }
}
