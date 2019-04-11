using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tetrix
{
    public class BlockCreater
    {
        public BlockType CreateBlocks(int type,int color, string direction) //create a composite block with a type, a direction and a color
        {
            BlockType block = new BlockType();
            Random ran = new Random();
            if(type == 0)
            {
                type = ran.Next(0, 10000) % 7 + 1;
            }
            if (color == 0)
            {
                color = ran.Next(0, 10000) % 7 + 2;
            }
            int initial_y = ran.Next(0, 10000) % 10 + 1;
            block.y = initial_y;
            block.TypeNumber = type;
            /* T1 up        right     down      left   
                  0 1 0     0 2 0     0 0 0     0 4 0
                  2 3 4  -  0 3 1  -  4 3 2  -  1 3 0
                  0 0 0     0 4 0     0 1 0     0 2 0 */
            if (type == 1)
            {
                if(direction == "up")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 2));
                }
                else if (direction == "right")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 1, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 1));
                }
                else if (direction == "down")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 2, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                }
                else if (direction == "left")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                }
            }
            /* T2 up        right     down      left   
                  1 0 0     3 2 1     0 4 3     0 0 0
                  2 0 0  -  4 0 0  -  0 0 2  -  0 0 4
                  3 4 0     0 0 0     0 0 1     1 2 3 */
            else if (type == 2)
            {
                if (direction == "up")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 0, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 1));
                }
                else if (direction == "right")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 0, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                }
                else if (direction == "down")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 2, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                }
                else if (direction == "left")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 2, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 2));
                }
            }
            /* T3 up        right     down      left   
                  0 0 1     0 0 0     3 4 0     1 2 3
                  0 0 2  -  4 0 0  -  2 0 0  -  0 0 4
                  0 4 3     3 2 1     1 0 0     0 0 0 */
            else if (type == 3)
            {
                if (direction == "up")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 0, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 1));
                }
                else if (direction == "right")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 2, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                }
                else if (direction == "down")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 2, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                }
                else if (direction == "left")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 0, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 2));
                }
            }
            /* T4 up        right     down      left   
                  1 0 0 0    1 2 3 4   up       right
                  2 0 0 0 -  0 0 0 0
                  3 0 0 0    0 0 0 0   
                  4 0 0 0    0 0 0 0 */
            else if (type == 4)
            {
                if (direction == "up" || direction == "down")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 3, 1));
                }
                else if (direction == "right" || direction == "left")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 3));
                }
            }
            /* T5 up        right     down      left   
                  1 2
                  3 4 */
            else if (type == 5)
            {
                block.BlockList.Add(new Block(block.x, block.y, 0, 0));
                block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                block.BlockList.Add(new Block(block.x, block.y, 1, 1));
            }
            /* T6 up        right     down      left   
                  1 0 0     0 2 1      up       right
                  2 3 0  -  4 3 0
                  0 4 0     0 0 0 */
            else if (type == 6)
            {
                if (direction == "up" || direction == "down")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 0, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 1));
                }
                else if (direction == "right" || direction == "left")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 0, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 0));
                }
            }
            /* T7 up        right     down      left   
                  0 0 1     1 2 0      up       right
                  0 3 2  -  0 3 4
                  0 4 0     0 0 0 */
            else if (type == 7)
            {
                if (direction == "up" || direction == "down")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 0, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 2));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 2, 1));
                }
                else if (direction == "right" || direction == "left")
                {
                    block.BlockList.Add(new Block(block.x, block.y, 0, 0));
                    block.BlockList.Add(new Block(block.x, block.y, 0, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 1));
                    block.BlockList.Add(new Block(block.x, block.y, 1, 2));
                }
            }
            block.Change_Color(color);
            return block;
        }
    }
}
