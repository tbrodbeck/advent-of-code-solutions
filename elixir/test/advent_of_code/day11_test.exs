defmodule AdventOfCode.Day11Test do
  use ExUnit.Case

  alias AdventOfCode.Day11

  @example_input """
  aaa: you hhh
  you: bbb ccc
  bbb: ddd eee
  ccc: ddd eee fff
  ddd: ggg
  eee: out
  fff: out
  ggg: out
  hhh: ccc fff iii
  iii: out
  """

  describe "part1/1" do
    test "solves example input" do
      assert Day11.part1(@example_input) == 5
    end
  end

  describe "part2/1" do
    test "solves example input" do
      assert Day11.part2(@example_input) == 0
    end
  end
end
