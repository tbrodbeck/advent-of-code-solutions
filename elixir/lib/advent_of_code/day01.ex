defmodule AdventOfCode.Day01 do
  @moduledoc """
  Day 1: Secret Entrance - Dial starts at 50, numbers 0-99 (circular).
  """

  def parse_input(input) do
    input
    |> String.trim()
    |> String.split("\n")
    |> Enum.map(&parse_line/1)
  end

  defp parse_line("R" <> rest), do: String.to_integer(rest)
  defp parse_line("L" <> rest), do: -String.to_integer(rest)

  def part1(input) do
    input
    |> parse_input()
    |> Enum.reduce({50, 0}, fn distance, {pos, count} ->
      new_pos = rem(pos + distance, 100)
      new_count = if new_pos == 0, do: count + 1, else: count
      {new_pos, new_count}
    end)
    |> elem(1)
  end

  def part2(input) do
    input
    |> parse_input()
    |> Enum.reduce({50, 0}, fn distance, {pos, count} ->
      new_pos = pos + distance
      crossings = count_zero_crossings(pos, new_pos)
      {Integer.mod(new_pos, 100), count + crossings}
    end)
    |> elem(1)
  end

  defp count_zero_crossings(prev, curr) do
    cond do
      prev < 100 and curr >= 100 -> div(curr, 100)
      curr <= 0 and prev > 0 -> div(-curr, 100) + 1
      prev == 0 and curr <= -100 -> div(-curr, 100)
      true -> 0
    end
  end
end
