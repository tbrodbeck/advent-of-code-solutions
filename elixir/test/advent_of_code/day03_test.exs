defmodule AdventOfCode.Day03Test do
  use ExUnit.Case

  alias AdventOfCode.Day03

  @example_input """
  987654321111111
  811111111111119
  234234234234278
  818181911112111
  """

  describe "part1/1" do
    test "solves example input" do
      assert Day03.part1(@example_input) == 357
    end

    test "max_joltage picks 2 largest digits in order" do
      assert Day03.max_joltage("987654321111111", 2) == 98
      assert Day03.max_joltage("811111111111119", 2) == 89
      assert Day03.max_joltage("818181911112111", 2) == 92
    end
  end

  describe "part2/1" do
    test "solves example input" do
      assert Day03.part2(@example_input) == 3_121_910_778_619
    end

    test "max_joltage picks 12 largest digits in order" do
      assert Day03.max_joltage("987654321111111", 12) == 987_654_321_111
      assert Day03.max_joltage("234234234234278", 12) == 434_234_234_278
      assert Day03.max_joltage("818181911112111", 12) == 888_911_112_111
    end
  end
end
