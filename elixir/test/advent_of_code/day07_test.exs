defmodule AdventOfCode.Day07Test do
  use ExUnit.Case

  alias AdventOfCode.Day07

  @example_input """
  ..S..
  ..^..
  .^.^.
  .....
  """

  describe "part1/1" do
    test "solves example input" do
      assert Day07.part1(@example_input) == 3
    end
  end

  describe "part2/1" do
    test "solves example input" do
      assert Day07.part2(@example_input) == 4
    end
  end
end
