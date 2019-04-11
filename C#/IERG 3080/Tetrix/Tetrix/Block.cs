using System;
using System.Collections.Generic;
using System.Windows.Forms;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tetrix
{
    public class Block // create an object represent a single block
    {
        public int TypeNumber; //represent which kind of block it is
        public int x; // the row of the block in the graph
        public int y; // the column of the block in the graph
        private int shift_x; // the shift of x direction corresponding to origin point of composite block 
        private int shift_y; // the shift of y direction corresponding to origin point of composite block 
        public string direction; // the direction "up down left right of the composite block block"
        public int color; // an interger between 0 to 8 corresponding to different color
        public Block()
        {
            this.TypeNumber = 0;
            this.x = 0;
            this.y = 0;
            this.shift_x = 0;
            this.shift_y = 0;
            this.color = 1;
            direction = "up";
        } // create a block
        public Block(int x0, int y0, int sx, int sy) //create a block with initial x,y and shift x,y 
        {
            this.TypeNumber = 0;
            this.x = x0 + sx;
            this.y = y0 + sy;
            this.shift_x = sx;
            this.shift_y = sy;
            this.color = 1;
            direction = "";
        } 
        public void SetPoint(int x0, int y0) // change the point of the block in the graph
        {
            shift(x0 - x, y0 - y);
            this.x = x0;
            this.y = y0;
        } 
        public virtual void shift(int shiftx, int shifty){ } //change the point of the sub-block corresponding to shift x,y
        public virtual void Change_Color(int color0) { this.color = color0; } // change the color of a single block
        public virtual void Draw(int[,] graph) // draw the block in the graph
        {
            graph[x, y] = color;
        } 
        public virtual void Remove(int[,] graph) // remove the block in the graph
        {
            graph[x, y] = 0;
        } 
        public void MoveAndDraw(int newX, int newY, int[,] graph) // set new point of a block then draw it
        {
            Remove(graph);
            SetPoint(newX, newY);
            Draw(graph);
        } 
        public string NextDierction(string d) // get the next directon corresponding to the clock-wise direction 
        {
            switch (d){
                case "up": return "right";
                case "right": return "down";
                case "down": return "left";
                case "left":return "up";
                default: return "";
            }       
        }  
        public virtual bool Is_out_of_range() // detect if the move and rotate operation cause out of range 
        {
            if (this.x >= 21 || this.y <= 0 || this.y >= 13)
                return true;
            else return false;
        } 
        public virtual bool Is_overlap(int [,] g) // detect if the move and rotate operation cause overlap
        {
            if (g[this.x, this.y] != 0)
                return true;
            return false;
        } 
        public virtual bool CanMove(int[,] graph,string direct) // detect if the block can be move without overlap or out of range
        {
            if (direct == "down")
            {
                if (graph[this.x + 1, this.y] != 0)
                    return false;
                else return true;
            }
            else if (direct == "left")
            {
                if (graph[this.x, this.y - 1] != 0 || this.y <= 1)
                    return false;
                else return true;
            }
            else if (direct == "right")
            {
                if (graph[this.x, this.y + 1] != 0 || this.y >= 12)
                    return false;
                else return true;
            }
            else return false;

        } 
        public virtual bool CanDraw(int[,] graph) // detect if the block can be draw without overlap or out of range
        {
            if (graph[x, y] == 1)
                return false;
            else return true;
        } 
        public bool isMyself(string Movedirection, List<Block> blockList) //check if the block under this block is myself or a pile block
        {
            foreach (Block block in blockList)
            {
                if (Movedirection == "down")
                {
                    if (this.shift_x + 1 == block.shift_x && this.shift_y == block.shift_y)
                        return true;
                }
                else if (Movedirection == "left")
                {
                    if (this.shift_x == block.shift_x && this.shift_y - 1 == block.shift_y)
                        return true;
                }
                else if (Movedirection == "right")
                {
                    if (this.shift_x == block.shift_x && this.shift_y + 1 == block.shift_y)
                        return true;
                }
            }
            return false;
        } 
        public virtual BlockType Rotated() { return new BlockType(); } // change the dirction of a block, set new bolck to replace it
    }
}
