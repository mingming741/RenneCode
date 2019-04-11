using System;
using System.Timers;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Tetrix
{
    public partial class Game_Form : Form
    {
        private Brush blue, yellow, black, white, green, purple, orange, red, cyan; // shows as 9 kind of colors
        private Rectangle[,] Shape = new Rectangle[22, 14]; // represent the block shape corresponding to the main container
        private Rectangle[,] Next_Shape = new Rectangle[5, 5]; // reprensent the next block shape 
        private int[,] next_block_graph = new int[5, 5]; // represnent the next block container
        private MyGraph g = new MyGraph(); // The main graph object of game
        private BlockCreater creater = new BlockCreater(); // the block creater to create block for rotated and new block
        private Block block, nextblock; // the reference of current block and newt block
        private string InitialDirection = "up"; // set up initial direction is up
        private static bool Restart = true; // the main control to start the game, when is become false the game start
        public static int Bonus = 0; // the score of the game
        public static bool pause = false; // the main control to pause the game
        private int Level = 2; // the level of the game    
        private int Time = 0; // the control timer to record the time event
        private int Time_Step = 100; // the time threshold of a time event
        
        public Game_Form() // intialize the form content 
        {           
            InitializeComponent();
            InitializeControl();
            InitializeForm();
        }
        public void InitializeForm() // initialize the color and the position of rectangle
        {
            blue = new SolidBrush(Color.Blue);
            yellow = new SolidBrush(Color.Yellow);
            black = new SolidBrush(Color.Black);
            white = new SolidBrush(Color.White);
            green = new SolidBrush(Color.Magenta);
            red = new SolidBrush(Color.Red);
            purple = new SolidBrush(Color.Violet);
            orange = new SolidBrush(Color.Lime);
            cyan = new SolidBrush(Color.BurlyWood);
            for (int i = 1; i <= 20; i++)
            {
                for (int j = 1; j <= 12; j++)
                {
                    int Legnth = 19;
                    Shape[i, j] = new Rectangle((Legnth + 1) * (j - 1) + 1, (Legnth + 1) * (i - 1) + 1, Legnth, Legnth);
                }
            }
            for (int i = 0; i < 4; i++)
            {
                for (int j = 0; j < 4; j++)
                {
                    int Legnth = 19;
                    Next_Shape[i, j] = new Rectangle((Legnth + 1) * (j + 1) + 1, (Legnth + 1) * (i + 1) + 1, Legnth, Legnth);
                }
            }
        }
        public void InitializeControl() // initialize the control variable
        {
            this.Game_Timer.Interval = 10;//1000 / (int)Math.Pow(2,Level) ;
            Level_label.Text = "Level " + Convert.ToString(Level);
            Bonus_label.Text = "Bonus " + Convert.ToString(Bonus);
        }
        private void Form1_Key_Event(object sender, KeyEventArgs e) // the operation "W A S D" for the users
        {
            if (Restart == true || pause == true)
                return;
            string operation = e.KeyCode.ToString();
            if (operation == "A")
            {
                if (block.CanMove(g.graph,"left"))
                {
                    block.MoveAndDraw(block.x, block.y - 1, g.graph);
                    ShowGraph();
                }
            }
            else if (operation == "D")
            {
                if (block.CanMove(g.graph, "right"))
                {
                    block.MoveAndDraw(block.x, block.y + 1, g.graph);
                    ShowGraph();
                }
            }
            else if (operation == "S")
            {
                if (block.CanMove(g.graph, "down"))
                {
                    block.MoveAndDraw(block.x + 1, block.y, g.graph);
                    ShowGraph();
                }
            }
            else if (operation == "W")
            {
                Block b = block.Rotated();
                block.Remove(g.graph);
                if (b.Is_out_of_range() == false && b.Is_overlap(g.graph) == false)
                {                
                    block = block.Rotated();
                }
                block.Draw(g.graph);
                ShowGraph();
            }
        }
        private void timer1_Tick(object sender, EventArgs e) // the main progress of the game
        {
            if(pause == false)
                Time = Time + (int)Math.Pow(2, Level);
            if (g.GameOver())
            {
                End();
                MessageBox.Show("Game Over!");
            }
            else if (Restart == false && Time >= Time_Step)
            {
                Time = 0;
                if (block.CanMove(g.graph, "down"))
                {
                    block.MoveAndDraw(block.x + 1, block.y, g.graph);
                    ShowGraph();
                    Show_Next_Block();
                }
                else if (g.GameOver())
                {
                    End();
                    MessageBox.Show("Game Over!");
                }
                else
                {
                    g.Remove_Line();
                    g.Reset_color();
                    Bonus_label.Text = "Bonus " + Convert.ToString(Bonus);
                    block = nextblock;
                    block.x = 0;
                    if(block.CanDraw(g.graph) == true && Restart == false)
                    {
                        block.Draw(g.graph);
                        nextblock = creater.CreateBlocks(0, 0, InitialDirection);
                        ShowGraph();
                        Show_Next_Block();
                    }
                    else
                    {
                        block.Draw(g.graph);
                        ShowGraph();
                        End();
                        MessageBox.Show("Game Over!");
                    }

                }
            }
        }
        public void ShowGraph() // the function to show the state of the container, using different kinds of block
        {
            Graphics g = Main_Screen.CreateGraphics();
            g.DrawLine(new Pen(black), new PointF(0, 0), new PointF(0, 400));
            g.DrawLine(new Pen(black), new PointF(0, 0), new PointF(240, 0));
            g.DrawLine(new Pen(black), new PointF(0, 400), new PointF(240, 400));
            g.DrawLine(new Pen(black), new PointF(240, 0), new PointF(240, 400));
            for (int i = 1; i <= 20; i++)
            {
                for (int j = 1; j <= 12; j++)
                {
                    if (this.g.graph[i, j] == 0)
                        g.FillRectangle(white, Shape[i, j]);
                    else if (this.g.graph[i, j] == 1)
                        g.FillRectangle(black , Shape[i, j]);
                    else if (this.g.graph[i, j] == 2)
                        g.FillRectangle(red, Shape[i, j]);
                    else if (this.g.graph[i, j] == 3)
                        g.FillRectangle(orange , Shape[i, j]);
                    else if (this.g.graph[i, j] == 4)
                        g.FillRectangle(yellow, Shape[i, j]);
                    else if (this.g.graph[i, j] == 5)
                        g.FillRectangle(green, Shape[i, j]);
                    else if (this.g.graph[i, j] == 6)
                        g.FillRectangle(cyan, Shape[i, j]);
                    else if (this.g.graph[i, j] == 7)
                        g.FillRectangle(blue, Shape[i, j]);
                    else if (this.g.graph[i, j] == 8)
                        g.FillRectangle(purple, Shape[i, j]);

                }
            }
        }
        public void Show_Next_Block() // the function to show the state of next block
        {
            for (int i = 0; i < 5; i++)
            {
                for (int j = 0; j < 5; j++)
                {
                    next_block_graph[i, j] = 0;
                }
            }
            int The_color = nextblock.color;
            if (nextblock.TypeNumber == 1)
            {
                next_block_graph[2, 3] = The_color;
                next_block_graph[3, 3] = The_color;
                next_block_graph[3, 2] = The_color;
                next_block_graph[3, 4] = The_color;
            }
            else if (nextblock.TypeNumber == 2)
            {
                next_block_graph[1, 2] = The_color;
                next_block_graph[2, 2] = The_color;
                next_block_graph[3, 2] = The_color;
                next_block_graph[3, 3] = The_color;
            }
            else if (nextblock.TypeNumber == 3)
            {
                next_block_graph[1, 3] = The_color;
                next_block_graph[2, 3] = The_color;
                next_block_graph[3, 2] = The_color;
                next_block_graph[3, 3] = The_color;
            }
            else if (nextblock.TypeNumber == 4)
            {
                next_block_graph[1, 2] = The_color;
                next_block_graph[2, 2] = The_color;
                next_block_graph[3, 2] = The_color;
                next_block_graph[4, 2] = The_color;
            }
            else if (nextblock.TypeNumber == 5)
            {
                next_block_graph[2, 2] = The_color;
                next_block_graph[2, 3] = The_color;
                next_block_graph[3, 2] = The_color;
                next_block_graph[3, 3] = The_color;
            }
            else if (nextblock.TypeNumber == 6)
            {
                next_block_graph[2, 2] = The_color;
                next_block_graph[4, 3] = The_color;
                next_block_graph[3, 2] = The_color;
                next_block_graph[3, 3] = The_color;
            }
            else if (nextblock.TypeNumber == 7)
            {
                next_block_graph[4, 2] = The_color;
                next_block_graph[2, 3] = The_color;
                next_block_graph[3, 2] = The_color;
                next_block_graph[3, 3] = The_color;
            }
            Graphics g0 = Next_Block.CreateGraphics();
            g0.DrawLine(new Pen(black), new PointF(0, 0), new PointF(0, 80));
            g0.DrawLine(new Pen(black), new PointF(0, 0), new PointF(80, 0));
            g0.DrawLine(new Pen(black), new PointF(0, 80), new PointF(80, 80));
            g0.DrawLine(new Pen(black), new PointF(80, 0), new PointF(80, 80));
            for (int i = 0; i < 5; i++)
            {
                for (int j = 0; j < 5; j++)
                {
                    if (next_block_graph[i, j] == 0)
                        g0.FillRectangle(white, Shape[i, j]);
                    else if (next_block_graph[i, j] == 1)
                        g0.FillRectangle(black, Shape[i, j]);
                    else if (next_block_graph[i, j] == 2)
                        g0.FillRectangle(red, Shape[i, j]);
                    else if (next_block_graph[i, j] == 3)
                        g0.FillRectangle(orange, Shape[i, j]);
                    else if (next_block_graph[i, j] == 4)
                        g0.FillRectangle(yellow, Shape[i, j]);
                    else if (next_block_graph[i, j] == 5)
                        g0.FillRectangle(green, Shape[i, j]);
                    else if (next_block_graph[i, j] == 6)
                        g0.FillRectangle(cyan, Shape[i, j]);
                    else if (next_block_graph[i, j] == 7)
                        g0.FillRectangle(blue, Shape[i, j]);
                    else if (next_block_graph[i, j] == 8)
                        g0.FillRectangle(purple, Shape[i, j]);

                }
            }
        }
        private void Pause_Lable_Click(object sender, EventArgs e) // the event of pause
        {
            if(Restart == false)
            {
                if (pause == false)
                {
                    pause = true;
                    Pause_Lable.Text = "Continue";
                }
                else if (pause == true)
                {
                    pause = false;
                    Pause_Lable.Text = "Pause";
                }
            }    
        }
        private void Exit_Lable_Click(object sender, EventArgs e){ this.Close(); } // the event of exit       
        private void Start_Botton_Click(object sender, EventArgs e) // the event of start
        {
            if(Restart == true)
            {
                Start();
                Start_Botton.Text = "End";
            }
            else if(Restart == false)
            {
                End();
                Main_Screen.Refresh();
                Next_Block.Refresh();
                Start_Botton.Text = "Start";
                MessageBox.Show("Game Over!");
                pause = false;
                Pause_Lable.Text = "Pause";
            }
            
        }
        private void Level_Up_Button_Click(object sender, EventArgs e) // the event of level up
        {
            if (Level < 6)
            {
                Level = Level + 1;
                Level_label.Text = "Level " + Convert.ToString(Level);
            }            
        }
        private void Level_Down_Botton_Click(object sender, EventArgs e) // the event of level down
        {
            if (Level > 1)
            {
                Level = Level - 1;
                Level_label.Text = "Level " + Convert.ToString(Level);
            }
        }
        public void Start() // the function of start the game
        {
            if (Restart == true)
            {
                Level = 2;
                Level_label.Text = "Level " + Convert.ToString(Level);
                block = creater.CreateBlocks(0, 0, InitialDirection);
                nextblock = creater.CreateBlocks(0, 0, InitialDirection);
                block.x = 0;
                block.Draw(g.graph);
            }
            Restart = false;
        }
        public void End() // the function of end the game
        {
            if (Restart == false)
            {
                Restart = true;
                g.Reset();
            }
        }
        void login_FormClosing(object sender, FormClosingEventArgs e) // the function for close the game window
        {
            Restart = true;
            g.Reset();
        }
    }
}