using System;
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
    public partial class Menu_Form : Form // The main menu of the game
    {
        public Menu_Form()
        {
            InitializeComponent();
        }
        private void Start_Button_Click(object sender, EventArgs e) // Start the game, run the game form
        {
            using (Game_Form form1 = new Game_Form())
            {
                form1.End();
                form1.Start(); 
                form1.ShowDialog();
            }
        }
        private void Read_Me_Button_Click(object sender, EventArgs e) // Tell the user the rule and operation of the game
        {
            string rules = "Rules\n";
            rules = rules + "1. A random sequence of these Blocks fall down one by one\n";
            rules = rules + "2. You can move the composite block either to the right or to the left,or rotate the Block in clockwise direction\n";
            rules = rules + "3. Block cannot overlap with other blocks. If a Block hits blocks, it stops. Once stopped, the blocks will then start to pile up\n";
            rules = rules + "4. If a horizontal row is full of blocks, then the entire row of blocks will be removed, you will get marks\n";
            rules = rules + "5. If the pile of blocks reach the top of the container, the game ends\n";
            MessageBox.Show(rules,"Rules");
            string shows = "Operations\n";
            shows = shows + "1. Rotate-W Down-S Left-A Right-D\n";
            shows = shows + "2. Click \"level up\" or \"level down\" to select the level\n";
            shows = shows + "3. Click \"pause\" to pause the game,and then click \"continue\" to restart\n";
            shows = shows + "4. Click \"End\" to end the current game,and then click \"start\" to start a new game\n";
            shows = shows + "5. Click \"Exit\" to return to the main menu\n";
            shows = shows + "Good Luck!";
            MessageBox.Show(shows,"Operations");
        }
        private void Exit_Button_Click(object sender, EventArgs e) // Exit the game
        {
            this.Close();
        }
    }
}
