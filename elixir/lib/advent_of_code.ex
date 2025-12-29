defmodule AdventOfCode do
  @moduledoc """
  Advent of Code solutions in Elixir.
  """

  @doc """
  Run a day's solution with input from file.

  Usage: `mix run -e 'AdventOfCode.solve(1)'`
  """
  def solve(day) do
    padded = String.pad_leading(Integer.to_string(day), 2, "0")
    module = Module.concat([AdventOfCode, :"Day#{padded}"])
    input = File.read!("inputs/day#{padded}.txt")

    IO.puts("Part 1: #{module.part1(input)}")
    IO.puts("Part 2: #{module.part2(input)}")
  end
end
