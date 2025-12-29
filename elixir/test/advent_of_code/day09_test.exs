defmodule AdventOfCode.Day09Test do
  use ExUnit.Case

  alias AdventOfCode.Day09

  @example_input """
  7,1
  11,1
  11,7
  9,7
  9,5
  2,5
  2,3
  7,3
  """

  describe "part1/1" do
    test "solves example input" do
      assert Day09.part1(@example_input) == 50
    end
  end

  describe "part2/1" do
    test "solves example input" do
      assert Day09.part2(@example_input) == 24
    end
  end
end
