defmodule AdventOfCode.Day03 do
  @moduledoc """
  Day 3: Lobby - Maximum joltage from battery banks.
  """

  def parse_input(input) do
    input
    |> String.trim()
    |> String.split("\n", trim: true)
  end

  @doc "Find max joltage by picking k digits in order."
  def max_joltage(bank, k) do
    digits = bank |> String.graphemes() |> Enum.map(&String.to_integer/1)
    n = length(digits)

    {result, _} =
      Enum.reduce(0..(k - 1)//1, {[], 0}, fn i, {acc, start} ->
        finish = n - k + i + 1
        {best_val, best_idx} = find_max(digits, start, finish)
        {acc ++ [best_val], best_idx + 1}
      end)

    result |> Enum.join() |> String.to_integer()
  end

  defp find_max(digits, start, finish) do
    start..(finish - 1)//1
    |> Enum.map(fn idx -> {Enum.at(digits, idx), idx} end)
    |> Enum.max_by(fn {val, _idx} -> val end)
  end

  defp solve(input, k) do
    input
    |> parse_input()
    |> Enum.map(&max_joltage(&1, k))
    |> Enum.sum()
  end

  def part1(input), do: solve(input, 2)
  def part2(input), do: solve(input, 12)
end
