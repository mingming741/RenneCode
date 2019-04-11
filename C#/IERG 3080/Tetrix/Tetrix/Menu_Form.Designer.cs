namespace Tetrix
{
    partial class Menu_Form
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(Menu_Form));
            this.Start_Button = new System.Windows.Forms.Button();
            this.Read_Me_Button = new System.Windows.Forms.Button();
            this.Exit_Button = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // Start_Button
            // 
            this.Start_Button.BackColor = System.Drawing.Color.Transparent;
            this.Start_Button.Cursor = System.Windows.Forms.Cursors.Hand;
            this.Start_Button.FlatAppearance.BorderSize = 0;
            this.Start_Button.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Start_Button.Font = new System.Drawing.Font("SketchFlow Print", 42F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Start_Button.Location = new System.Drawing.Point(34, 12);
            this.Start_Button.Name = "Start_Button";
            this.Start_Button.Size = new System.Drawing.Size(213, 79);
            this.Start_Button.TabIndex = 0;
            this.Start_Button.Text = "Start";
            this.Start_Button.UseVisualStyleBackColor = false;
            this.Start_Button.Click += new System.EventHandler(this.Start_Button_Click);
            // 
            // Read_Me_Button
            // 
            this.Read_Me_Button.BackColor = System.Drawing.Color.Transparent;
            this.Read_Me_Button.Cursor = System.Windows.Forms.Cursors.Hand;
            this.Read_Me_Button.FlatAppearance.BorderSize = 0;
            this.Read_Me_Button.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Read_Me_Button.Font = new System.Drawing.Font("SketchFlow Print", 42F);
            this.Read_Me_Button.Location = new System.Drawing.Point(12, 97);
            this.Read_Me_Button.Name = "Read_Me_Button";
            this.Read_Me_Button.Size = new System.Drawing.Size(260, 75);
            this.Read_Me_Button.TabIndex = 1;
            this.Read_Me_Button.Text = "Declare";
            this.Read_Me_Button.UseVisualStyleBackColor = false;
            this.Read_Me_Button.Click += new System.EventHandler(this.Read_Me_Button_Click);
            // 
            // Exit_Button
            // 
            this.Exit_Button.BackColor = System.Drawing.Color.Transparent;
            this.Exit_Button.Cursor = System.Windows.Forms.Cursors.Hand;
            this.Exit_Button.FlatAppearance.BorderSize = 0;
            this.Exit_Button.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.Exit_Button.Font = new System.Drawing.Font("SketchFlow Print", 42F);
            this.Exit_Button.Location = new System.Drawing.Point(25, 178);
            this.Exit_Button.Name = "Exit_Button";
            this.Exit_Button.Size = new System.Drawing.Size(235, 72);
            this.Exit_Button.TabIndex = 2;
            this.Exit_Button.Text = "Exit";
            this.Exit_Button.UseVisualStyleBackColor = false;
            this.Exit_Button.Click += new System.EventHandler(this.Exit_Button_Click);
            // 
            // Form2
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 12F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.BackgroundImage = ((System.Drawing.Image)(resources.GetObject("$this.BackgroundImage")));
            this.ClientSize = new System.Drawing.Size(284, 262);
            this.Controls.Add(this.Exit_Button);
            this.Controls.Add(this.Read_Me_Button);
            this.Controls.Add(this.Start_Button);
            this.Name = "Form2";
            this.Text = "Tetrix";
            this.ResumeLayout(false);

        }

        #endregion

        private System.Windows.Forms.Button Start_Button;
        private System.Windows.Forms.Button Read_Me_Button;
        private System.Windows.Forms.Button Exit_Button;
    }
}