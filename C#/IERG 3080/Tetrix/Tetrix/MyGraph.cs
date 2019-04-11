using System;
using System.Windows.Forms;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace Tetrix
{
    public class MyGraph
    {
        public int[,] graph = new int[22, 14]; // represnent 20 x 12 graph, another blanks are preserve to handle the out of range problem
        public MyGraph() // initialize the graph
        {
            for (int i = 0; i <= 20; i++)
            {
                for (int j = 0; j < 14; j++)
                {
                    graph[i, j] = 0;
                }
            }
            for (int j = 0; j < 14; j++)
            {
                graph[21, j] = 1;
            }
        }
        public void Remove_Line() // if a row is filled with block, remove it and all the row up to it will drop for one line
        {
            bool Re_Remove = false;
            if (Can_Remove() != 0)
            {
                Re_Remove = true;
                Game_Form.Bonus = Game_Form.Bonus + 1;
                int line = Can_Remove();
                for(int i = line; i > 1; i--)
                {
                    for(int j = 1;j < 12; j++)
                    {
                        graph[i, j] = graph[i-1, j];
                    }
                }
                for (int j = 1; j < 12; j++)
                {
                    graph[1, j] = 0;
                }
            }             
            if (Re_Remove == true)
                this.Remove_Line();
        }
        public int Can_Remove() // check if there is a line should be remove
        {
            int Move_Line = 0;          
            for(int i = 1;i <= 20; i++)
            {
                int total = 0;
                for (int j = 1;j <= 12; j++)
                {
                    if(this.graph [i,j] != 0)
                    {
                        total++;
                    }
                }
                if (total == 12)
                {
                    Move_Line = i;
                    break;
                }                  
            }
            return Move_Line;
        }
        public bool GameOver() // check the condition if the block are pile up to the top of the container
        {
            for (int j = 1; j < 13; j++)
            {
                if (graph[1, j] == 1)
                    return true;
            }
            return false;
        }
        public void Reset_color() // change color for all the block in the container
        {
            for (int i = 0; i < 21; i++)
            {
                for (int j = 0; j < 14; j++)
                {
                    if (graph[i, j] != 0)
                        graph[i, j] = 1;
                }
            }
        }
        public void Reset() //Reset the container
        {
            for (int i = 0; i < 21; i++)
            {
                for (int j = 0; j < 14; j++)
                {
                    graph[i, j] = 0;
                }
            }
        }
    }
}
