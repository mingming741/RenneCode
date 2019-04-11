using System;
using System.Drawing;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tetrix
{
    public class BlockType : Block
    {
        public List<Block> BlockList; // a composite block contain a list of single block
        public BlockType() : base()
        {
            BlockList = new List<Block>();
        }
        public override void Change_Color(int color0) // change the color of a composite block 
        {
            foreach (Block block in BlockList)
            {
                block.Change_Color(color0);
            }
        } 
        public override void Draw(int[,] graph) // draw the composite block in the graph
        {
            foreach (Block block in BlockList)
            {
                block.Draw(graph);
            }
        } 
        public override void Remove(int[,] graph)  // remove the composite block in the graph
        {
            foreach (Block block in BlockList)
            {
                block.Remove(graph);
            }
        } 
        public override bool Is_out_of_range()
        {
            foreach (Block block in BlockList)
            {
                if (block.Is_out_of_range() == true)
                    return true;
            }
            return false;
        } // detect if the move and rotate operation cause out of range
        public override bool Is_overlap(int[,] g)
        {
            foreach (Block block in BlockList)
            {
                if (block.Is_overlap(g) == true)
                    return true;
            }
            return false;
        } // detect if the move and rotate operation cause overlap
        public override bool CanDraw(int[,] g)
        {
            foreach (Block block in BlockList)
            {
                if (block.CanDraw(g) == false)
                    return false;
            }
            return true;
        }  // detect if the block can be draw without overlap or out of range
        public override bool CanMove(int[,] graph,string direct)
        {
            for (int i = 0; i < 4; i++)
            {
                if(direct == "down")
                {
                    if (BlockList[i].CanMove(graph,"down") == false && !BlockList[i].isMyself("down", this.BlockList))
                        return false;
                }
                else if(direct == "left")
                {
                    if (BlockList[i].CanMove(graph,"left") == false && !BlockList[i].isMyself("left", this.BlockList))
                        return false;
                }
                else if (direct == "right")
                {
                    if (BlockList[i].CanMove(graph, "right") == false && !BlockList[i].isMyself("right", this.BlockList))
                        return false;
                }
            }
            return true;
        } // detect if the block can be move without draw or out of range
        public override void shift(int shiftx, int shifty) //change the point of the all the sub-block corresponding to shift x,y
        {
            foreach (Block block in BlockList)
            {
                block.x = block.x + shiftx;
                block.y = block.y + shifty;
            }
        } 
        public override BlockType Rotated()
        {
            BlockCreater creater = new BlockCreater();
            Block block = new Block();
            string nextDirection = this.NextDierction(this.direction);
            block = creater.CreateBlocks(TypeNumber,BlockList[0].color, nextDirection);
            block.SetPoint(this.x, this.y);
            block.direction = nextDirection;
            return (BlockType)block;
        }  // change the dirction of a block, set new bolck to replace it
    }
}
