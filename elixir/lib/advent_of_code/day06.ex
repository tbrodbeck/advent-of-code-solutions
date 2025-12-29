defmodule AdventOfCode.Day06 do
  @moduledoc """
  Day 6: Trash Compactor - Solve cephalopod math problems.
  """

  def parse_input(input) do
    lines =
      input
      |> String.split("\n")
      |> Enum.filter(&(String.trim(&1) != ""))

    max_width = lines |> Enum.map(&String.length/1) |> Enum.max()
    padded = Enum.map(lines, &String.pad_trailing(&1, max_width))

    {operation_line, number_lines} = List.pop_at(padded, -1)
    {number_lines, operation_line, max_width}
  end

  defp find_boundaries(padded, max_width) do
    find_boundaries(padded, max_width, 0, [])
  end

  defp find_boundaries(_padded, max_width, i, acc) when i >= max_width do
    Enum.reverse(acc)
  end

  defp find_boundaries(padded, max_width, i, acc) do
    # Skip separator columns
    i = skip_spaces(padded, max_width, i)

    if i >= max_width do
      Enum.reverse(acc)
    else
      start_col = i
      end_col = find_end(padded, max_width, i)
      find_boundaries(padded, max_width, end_col, [{start_col, end_col} | acc])
    end
  end

  defp skip_spaces(_padded, max_width, i) when i >= max_width, do: i

  defp skip_spaces(padded, max_width, i) do
    if all_spaces?(padded, i), do: skip_spaces(padded, max_width, i + 1), else: i
  end

  defp find_end(_padded, max_width, i) when i >= max_width, do: i

  defp find_end(padded, max_width, i) do
    if all_spaces?(padded, i), do: i, else: find_end(padded, max_width, i + 1)
  end

  defp all_spaces?(lines, col) do
    Enum.all?(lines, fn line -> String.at(line, col) == " " end)
  end

  # Part 1: horizontal reading, left-to-right
  defp extract_numbers_part1(number_lines, start_col, end_col) do
    number_lines
    |> Enum.map(fn line ->
      segment = String.slice(line, start_col, end_col - start_col)
      case Regex.run(~r/\d+/, segment) do
        [num] -> String.to_integer(num)
        _ -> nil
      end
    end)
    |> Enum.reject(&is_nil/1)
  end

  defp extract_operation_part1(operation_line, start_col, end_col) do
    segment = String.slice(operation_line, start_col, end_col - start_col) |> String.trim()
    if segment != "", do: String.first(segment), else: nil
  end

  # Part 2: vertical reading, right-to-left
  defp extract_numbers_part2(number_lines, start_col, end_col) do
    (end_col - 1)..start_col//-1
    |> Enum.map(fn col ->
      digits =
        number_lines
        |> Enum.map(&String.at(&1, col))
        |> Enum.filter(&(&1 != nil and &1 =~ ~r/\d/))
        |> Enum.join()

      if digits != "", do: String.to_integer(digits), else: nil
    end)
    |> Enum.reject(&is_nil/1)
    |> Enum.reverse()
  end

  defp extract_operation_part2(operation_line, start_col, end_col) do
    (end_col - 1)..start_col//-1
    |> Enum.find_value(fn col ->
      char = String.at(operation_line, col)
      if char in ["+", "*"], do: char, else: nil
    end)
  end

  defp solve_problem(numbers, "+"), do: Enum.sum(numbers)
  defp solve_problem(numbers, "*"), do: Enum.product(numbers)

  def part1(input) do
    {number_lines, operation_line, max_width} = parse_input(input)
    padded = number_lines ++ [operation_line]
    boundaries = find_boundaries(padded, max_width)

    boundaries
    |> Enum.map(fn {s, e} ->
      numbers = extract_numbers_part1(number_lines, s, e)
      op = extract_operation_part1(operation_line, s, e)
      if numbers != [] and op, do: solve_problem(numbers, op), else: 0
    end)
    |> Enum.sum()
  end

  def part2(input) do
    {number_lines, operation_line, max_width} = parse_input(input)
    padded = number_lines ++ [operation_line]
    boundaries = find_boundaries(padded, max_width)

    boundaries
    |> Enum.reverse()
    |> Enum.map(fn {s, e} ->
      numbers = extract_numbers_part2(number_lines, s, e)
      op = extract_operation_part2(operation_line, s, e)
      if numbers != [] and op, do: solve_problem(numbers, op), else: 0
    end)
    |> Enum.sum()
  end
end
