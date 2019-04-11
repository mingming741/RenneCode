using System;using System.Drawing;using System.Collections;using System.ComponentModel;using System.Windows.Forms;using System.Data;
namespace Tetrix
{
    partial class Game_Form
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Game_Form));
            this.Main_Screen = new System.Windows.Forms.Panel();
            this.Start_Botton = new System.Windows.Forms.Button();
            this.Level_Up_Button = new System.Windows.Forms.Button();
            this.Level_Down_Botton = new System.Windows.Forms.Button();
            this.Level_label = new System.Windows.Forms.Label();
            this.Bonus_label = new System.Windows.Forms.Label();
            this.Game_Timer = new System.Windows.Forms.Timer(this.components);
            this.Next_Block = new System.Windows.Forms.Panel();
            this.label1 = new System.Windows.Forms.Label();
            this.label2 = new System.Windows.Forms.Label();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.Pause_Lable = new System.Windows.Forms.Label();
            this.Exit_Lable = new System.Windows.Forms.Label();
            this.Next_lable = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // Main_Screen
            // 
            this.Main_Screen.BackColor = System.Drawing.Color.Transparent;
            this.Main_Screen.Location = new System.Drawing.Point(22, 72);
            this.Main_Screen.Name = "Main_Screen";
            this.Main_Screen.Size = new System.Drawing.Size(247, 429);
            this.Main_Screen.TabIndex = 0;
            // 
            // Start_Botton
            // 
            this.Start_Botton.BackColor = System.Drawing.Color.Transparent;
            this.Start_Botton.Cursor = System.Windows.Forms.Cursors.Hand;
            this.Start_Botton.FlatAppearance.BorderColor = System.Drawing.Color.White;
            this.Start_Botton.FlatAppearance.BorderSize = 0;
            this.Start_Botton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.Start_Botton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.Start_Botton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Start_Botton.Font = new System.Drawing.Font("Buxton Sketch", 26.25F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Start_Botton.Location = new System.Drawing.Point(12, 12);
            this.Start_Botton.Name = "Start_Botton";
            this.Start_Botton.Size = new System.Drawing.Size(92, 41);
            this.Start_Botton.TabIndex = 1;
            this.Start_Botton.Text = "End";
            this.Start_Botton.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.Start_Botton.UseVisualStyleBackColor = false;
            this.Start_Botton.Click += new System.EventHandler(this.Start_Botton_Click);
            // 
            // Level_Up_Button
            // 
            this.Level_Up_Button.BackColor = System.Drawing.Color.Transparent;
            this.Level_Up_Button.Cursor = System.Windows.Forms.Cursors.Hand;
            this.Level_Up_Button.FlatAppearance.BorderSize = 0;
            this.Level_Up_Button.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.Level_Up_Button.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.Level_Up_Button.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Level_Up_Button.Font = new System.Drawing.Font("Buxton Sketch", 15.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Level_Up_Button.Location = new System.Drawing.Point(269, 175);
            this.Level_Up_Button.Name = "Level_Up_Button";
            this.Level_Up_Button.Size = new System.Drawing.Size(92, 36);
            this.Level_Up_Button.TabIndex = 3;
            this.Level_Up_Button.Text = "Level up";
            this.Level_Up_Button.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.Level_Up_Button.UseVisualStyleBackColor = false;
            this.Level_Up_Button.Click += new System.EventHandler(this.Level_Up_Button_Click);
            // 
            // Level_Down_Botton
            // 
            this.Level_Down_Botton.BackColor = System.Drawing.Color.Transparent;
            this.Level_Down_Botton.Cursor = System.Windows.Forms.Cursors.Hand;
            this.Level_Down_Botton.FlatAppearance.BorderSize = 0;
            this.Level_Down_Botton.FlatAppearance.MouseDownBackColor = System.Drawing.Color.Transparent;
            this.Level_Down_Botton.FlatAppearance.MouseOverBackColor = System.Drawing.Color.Transparent;
            this.Level_Down_Botton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Level_Down_Botton.Font = new System.Drawing.Font("Buxton Sketch", 15.75F);
            this.Level_Down_Botton.Location = new System.Drawing.Point(269, 217);
            this.Level_Down_Botton.Name = "Level_Down_Botton";
            this.Level_Down_Botton.Size = new System.Drawing.Size(101, 30);
            this.Level_Down_Botton.TabIndex = 4;
            this.Level_Down_Botton.Text = "Level down";
            this.Level_Down_Botton.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.Level_Down_Botton.UseVisualStyleBackColor = false;
            this.Level_Down_Botton.Click += new System.EventHandler(this.Level_Down_Botton_Click);
            // 
            // Level_label
            // 
            this.Level_label.AutoSize = true;
            this.Level_label.BackColor = System.Drawing.Color.Transparent;
            this.Level_label.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Level_label.Font = new System.Drawing.Font("Buxton Sketch", 15.75F);
            this.Level_label.Location = new System.Drawing.Point(275, 272);
            this.Level_label.Name = "Level_label";
            this.Level_label.Size = new System.Drawing.Size(48, 26);
            this.Level_label.TabIndex = 5;
            this.Level_label.Text = "Level";
            this.Level_label.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // Bonus_label
            // 
            this.Bonus_label.AutoSize = true;
            this.Bonus_label.BackColor = System.Drawing.Color.Transparent;
            this.Bonus_label.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Bonus_label.Font = new System.Drawing.Font("Buxton Sketch", 15.75F);
            this.Bonus_label.Location = new System.Drawing.Point(275, 317);
            this.Bonus_label.Name = "Bonus_label";
            this.Bonus_label.Size = new System.Drawing.Size(62, 26);
            this.Bonus_label.TabIndex = 6;
            this.Bonus_label.Text = "Bonus";
            this.Bonus_label.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // Game_Timer
            // 
            this.Game_Timer.Enabled = true;
            this.Game_Timer.Interval = 1000;
            this.Game_Timer.Tick += new System.EventHandler(this.timer1_Tick);
            // 
            // Next_Block
            // 
            this.Next_Block.BackColor = System.Drawing.Color.Transparent;
            this.Next_Block.Location = new System.Drawing.Point(280, 72);
            this.Next_Block.Name = "Next_Block";
            this.Next_Block.Size = new System.Drawing.Size(87, 86);
            this.Next_Block.TabIndex = 7;
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.BackColor = System.Drawing.Color.Transparent;
            this.label1.Font = new System.Drawing.Font("Buxton Sketch", 15.75F);
            this.label1.Location = new System.Drawing.Point(7, 504);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(97, 26);
            this.label1.TabIndex = 8;
            this.label1.Text = "Rotated: W";
            this.label1.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.BackColor = System.Drawing.Color.Transparent;
            this.label2.Font = new System.Drawing.Font("Buxton Sketch", 15.75F);
            this.label2.Location = new System.Drawing.Point(126, 504);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(61, 26);
            this.label2.TabIndex = 9;
            this.label2.Text = "Left: A";
            this.label2.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.BackColor = System.Drawing.Color.Transparent;
            this.label3.Font = new System.Drawing.Font("Buxton Sketch", 15.75F);
            this.label3.Location = new System.Drawing.Point(193, 504);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(75, 26);
            this.label3.TabIndex = 10;
            this.label3.Text = "Right: D";
            this.label3.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.BackColor = System.Drawing.Color.Transparent;
            this.label4.Font = new System.Drawing.Font("Buxton Sketch", 15.75F);
            this.label4.Location = new System.Drawing.Point(290, 504);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(77, 26);
            this.label4.TabIndex = 11;
            this.label4.Text = "Down: S";
            this.label4.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // Pause_Lable
            // 
            this.Pause_Lable.AutoSize = true;
            this.Pause_Lable.BackColor = System.Drawing.Color.Transparent;
            this.Pause_Lable.Cursor = System.Windows.Forms.Cursors.Hand;
            this.Pause_Lable.Font = new System.Drawing.Font("Buxton Sketch", 21.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Pause_Lable.Location = new System.Drawing.Point(96, 12);
            this.Pause_Lable.Name = "Pause_Lable";
            this.Pause_Lable.Size = new System.Drawing.Size(76, 36);
            this.Pause_Lable.TabIndex = 12;
            this.Pause_Lable.Text = "Pause";
            this.Pause_Lable.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.Pause_Lable.Click += new System.EventHandler(this.Pause_Lable_Click);
            // 
            // Exit_Lable
            // 
            this.Exit_Lable.AutoSize = true;
            this.Exit_Lable.BackColor = System.Drawing.Color.Transparent;
            this.Exit_Lable.Cursor = System.Windows.Forms.Cursors.Hand;
            this.Exit_Lable.Font = new System.Drawing.Font("Buxton Sketch", 21.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Exit_Lable.Location = new System.Drawing.Point(192, 16);
            this.Exit_Lable.Name = "Exit_Lable";
            this.Exit_Lable.Size = new System.Drawing.Size(53, 36);
            this.Exit_Lable.TabIndex = 13;
            this.Exit_Lable.Text = "Exit";
            this.Exit_Lable.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.Exit_Lable.Click += new System.EventHandler(this.Exit_Lable_Click);
            // 
            // Next_lable
            // 
            this.Next_lable.AutoSize = true;
            this.Next_lable.BackColor = System.Drawing.Color.Transparent;
            this.Next_lable.Cursor = System.Windows.Forms.Cursors.Arrow;
            this.Next_lable.Font = new System.Drawing.Font("Buxton Sketch", 21.75F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Next_lable.Location = new System.Drawing.Point(293, 16);
            this.Next_lable.Name = "Next_lable";
            this.Next_lable.Size = new System.Drawing.Size(61, 36);
            this.Next_lable.TabIndex = 14;
            this.Next_lable.Text = "Next";
            this.Next_lable.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            // 
            // Form1
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("$this.BackgroundImage")));
            this.BackgroundImageLayout = System.Windows.Forms.ImageLayout.None;
            this.ClientSize = new System.Drawing.Size(373, 539);
            this.Controls.Add(this.Next_lable);
            this.Controls.Add(this.Exit_Lable);
            this.Controls.Add(this.Pause_Lable);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.Next_Block);
            this.Controls.Add(this.Bonus_label);
            this.Controls.Add(this.Level_label);
            this.Controls.Add(this.Level_Down_Botton);
            this.Controls.Add(this.Level_Up_Button);
            this.Controls.Add(this.Start_Botton);
            this.Controls.Add(this.Main_Screen);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedSingle;
            this.KeyPreview = true;
            this.Name = "Form1";
            this.Text = "Tetrix";
            this.KeyDown += new System.Windows.Forms.KeyEventHandler(this.Form1_Key_Event);
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Panel Main_Screen;
        private System.Windows.Forms.Button Start_Botton;
        private Button Level_Up_Button;
        private Button Level_Down_Botton;
        public Label Level_label;
        private Label Bonus_label;
        public Timer Game_Timer;
        private Panel Next_Block;
        private Label label1;
        private Label label2;
        private Label label3;
        private Label label4;
        private Label Pause_Lable;
        private Label Exit_Lable;
        private Label Next_lable;
    }
}

