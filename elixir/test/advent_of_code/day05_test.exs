defmodule AdventOfCode.Day05Test do
  use ExUnit.Case

  alias AdventOfCode.Day05

  @example_input """
  1-5
  10-15
  3-8

  2
  7
  9
  12
  """

  describe "part1/1" do
    test "solves example input" do
      assert Day05.part1(@example_input) == 3
    end

    test "is_fresh?" do
      ranges = [{1, 5}, {10, 15}]
      assert Day05.fresh?(3, ranges)
      assert Day05.fresh?(12, ranges)
      refute Day05.fresh?(7, ranges)
    end
  end

  describe "part2/1" do
    test "solves example input" do
      assert Day05.part2(@example_input) == 14
    end
  end
end
