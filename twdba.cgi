#! /usr/bin/perl -w

#===============================
#
# Todo:
#
# Tables_Menu_Copy_Table
# Tables_Menu_Alter_Table
# Help System & User documentation
#
#===============================

use CGI;
use DBI;

$q = new CGI;

# ==================================================================================================================

$TWDBAVersion = '1.2.2';
$DebugLevel  = 'Tru';
$DisableLogin = 'Tru';
$InitializedFirstSession = 'False';
$ConfigurationPath = '/var/tmp';
$ConfigurationFile = 'twdba.conf';
$InitializedFirstSessionMessage = 'Welcome to Typhoon Web DataBase Administrator '.$TWDBAVersion.'.\nA little requirement is to have perl modules: CGI and DBI\nTWDBA automatically finds installed DBD drivers as you install them.\nTWDBA automatically generates a (local)host entry with mysql.\nThis is just to use TWDBA right away locally with MySQL\nThis program is still under construction.\nHere is list of things that I still need TODO:\n\nTables_Menu_Copy_Table\nTables_Menu_Alter_Table\nHelp System & User documentation\n\nPlease be patient, Im allmost updating daily\nYou can also click Email Author to drop me an email\nEnjoy Typhoon Web DataBase Administrator as it is Open Source!!!\n\nKind Regards,\n\n\nRon de Jong from Holland (Windmill & Cloggyland)';

my $Black          = '#000000';
my $White          = '#FFFFFF';
my $Grey           = '#DCDCCC';
my $DarkGrey       = '#BABAAA';
my $UltraDarkGrey  = '#878777';
my $Red            = '#FF0000';
my $RedGrey        = '#F0DCCC';
my $Green          = '#00FF00';
my $GreenGrey      = '#DCE4CC';
my $Blue           = '#0000FF';
my $LightBlue      = '#33CCFF';
my $UltraLightBlue = '#7777FF';
my $SoftBlue       = '#4466DD';
my $BlueGrey       = '#DCDCDD';
my $DarkBlue       = '#000099';
my $UltraDarkBlue  = '#000033';
my $CloudBlue      = '#446688';
my $Orange         = '#FFAA00';
my $OrangeGrey     = '#EFDFC4';
my $Yellow         = '#FFFF00';

@DBFieldTypes = (
CHAR,NUMERIC,DECIMAL,INTEGER,SMALLINT,FLOAT,REAL,DOUBLE,DATE,TIME,TIMESTAMP,VARCHAR,BIGINT,TINYINT,BIT);

@SizelessDBFieldTypes = (
NUMERIC,DECIMAL,INTEGER,SMALLINT,FLOAT,REAL,DOUBLE,DATE,TIME,TIMESTAMP,BIGINT,TINYINT);

=head1 PRODUCT

Typhoon Web DataBase Administrator 1.2.2

=head1 DESCRIPTION

Typhoon-Web-DataBase-Administrator-1.2.2 is a very easy to use, sexy, powerful and extremely userfriendly Database Administration Web-Program.
It can administrate remote Database Servers by simply Adding an Hostname or IP-Address and select a Database type.
Then fill in your Database username and password in the newly created host entry and start working with twdba.cgi
For detailed description of what Typhoon-Web-DataBase-Administrator-1.2.2 is all about the screenshots of twdba.html
It is also capable of copying an entire Database to an Empty Database in a snap. You will see how sexy, easy and powerfull this is!!!
Drop me an email if you wish: radejong@planet.nl
Regards, Ron de Jong from Holland (Windmill & Cloggyland).


=head1 PREREQUISITES

This script requires the CGI and DBI

=head1 COREQUISITES

To operate this script you need:

Apache

DBD::dbdriver

=head1 FILES

Typhoon-Web-DataBase-Administrator-1.2.2.tar.gz

The tarball contains the following file:

twdba-1.2.2/README     (explanation)

twdba-1.2.2/twdba.cgi  (program)

twdba-1.2.2/twdba.html (Screenshots)

=head1 INSTALLATION

To install TWDBA, just copy Typhoon-Web-Database-1.?.?.tar.gz to a temp directory
Such as /var/tmp and type the following:
gzip -cd Typhoon-Web-Database-1.?.?.tar.gz | tar xvf -
This will create a directory called twdba-1.?.?
Go into the directory and copy twdba.cgi to your cgi-bin directory of your HTTP server
Often this will be /usr/local/apache/cgi-bin/
The only thing left is to set the owner and filepermissions correct.
The owner shout be the user that is also running httpd (web-server)
A quick "ps -ef | grep httpd" will give you the releated username
Type chown nobody:nobody /usr/local/apache/cgi-bin/twdba.cgi
Type chmod 740 /usr/local/apache/cgi-bin/twdba.cgi
The above will set nobody nobody rwx r-- --- twdba.cgi (nobody is an advised httpd user).

=pod OSNAMES

any

=pod SCRIPT CATEGORIES

CGI
CPAN/Administrative
Networking
Fun/Educational
Web Interfaces

=cut

# ==================================================================================================================

print $q->header;
if ( $DebugLevel =~ '^True$' )
{
   print $q->start_html( -title => "Typhoon Web DataBase Administator",
                         -meta => {'keywords' => 'database db mysql oracle informix sybase msql sql'},
                         -bgcolor => "$SoftBlue" );
}
else
{
   print $q->start_html( -title => "Typhoon Web DataBase Administator",
                         -meta => {'keywords' => 'database db mysql oracle informix sybase msql sql'},
                         -bgcolor => "$UltraDarkBlue" );
}
print $q->start_html( -title => "Typhoon Web DataBase Administator",
                      -meta => {'keywords' => 'database db mysql oracle informix sybase msql sql'},
                      -bgcolor => "$UltraDarkBlue" );

Javascript_Function_Initializer();
Form_Phase_Selector();

# ==================================================================================================================

sub Javascript_Function_Initializer
{
   if ( $DebugLevel =~ '^True$' )
   {
      print "Started Javascript_Function_Initializer<br>\n";
   }
   print "<script language=\"JavaScript\">\n";
   print "<!--\n";

   print "function DoConfirm(Message)\n";
   print "{\n";
   print "   if (confirm (Message))\n";
   print "   {\n";
   print "      document.Generic_Form.submit()\;\n";
   print "   }\n";
   print "   else\n";
   print "   {\n";
   print "      document.write('')\;\n";
   print "   }\n";
   print "}\n";

   print "function Email_Author()\n";
   print "{\n";
   print "      window.location.href=\'mailto:radejong\@planet.nl?subject=TWDBA: \'\;\n";
   print "}\n";

   print "//-->\n";
   print "</script>\n";
}
# ==================================================================================================================

sub Error_Message
{
   foreach $ParamaterEntry (@_)
   {
      $ParamaterEntriesString .= $ParamaterEntry." ";
   }
   $_ .= $ParamaterEntriesString;
   print "<script language=\"JavaScript\">\n";
   print "<!--\n";
   s/'/"/g;
      print "      alert(\'$_\')\;\n";
   print "//-->\n";
   print "</script>\n";
}

# ==================================================================================================================

sub Generic_Message
{
   print "<script language=\"JavaScript\">\n";
   print "<!--\n";
   print "      window.status = '$LastErrorMessage'\;\n";
   print "//-->\n";
   print "</script>\n";
}

# ==================================================================================================================

sub Display_Parameters
{
   if ( $DebugLevel =~ '^True$' )
   {
      print "Started Display Parameters<br>\n";
   }
   print "<br>\n";
   print "<TABLE>\n";
   print "<TR>\n";
   print "<TD><font color=\"FF0000\">Parameter</font></TD>\n";
   print "<TD><font color=\"FF0000\">Value</font></TD>\n";
   print "</TR>\n";
   foreach $ParamEntry ($q->param)
   {
      if ($q->param($ParamEntry))
      {
         print "<TR>\n";
         $ParamEntryValue = $q->param($ParamEntry);
         print "<TD><font color=\"00FF00\">$ParamEntry</font></TD>\n";
         print "<TD><font color=\"00FF00\">$ParamEntryValue</font></TD>\n";
         print "</TR>\n";
      }
   }
   print "</TABLE>\n";
   print "<br>\n";
}

# ==================================================================================================================

sub Display_Navigation_Bar
{
   if ( $DebugLevel =~ '^True$' )
   {
      print "Started Display_Navigation_Bar<br>\n";
   }

  # Print Title
  print "<TABLE BGCOLOR=\"$Grey\" width=\"100%\" ALIGN=\"center\" BORDER=\"1\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH colspan=7 bgcolor=\"$UltraLightBlue\" ><font color=\"$White\"><br><big><big><big><big><big><big><font color=\"$Yellow\">T</font></big></big></big>yphoon <big><big><big><font color=\"$Yellow\">W</font></big></big></big>eb <big><big><big><font color=\"$Yellow\">D</font></big></big></big>ata<big><big><big><font color=\"$Yellow\">B</font></big></big></big>ase <big><big><big><font color=\"$Yellow\">A</font></big></big></big>dministrator $TWDBAVersion<br><br></font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\" COLSPAN = 7><font color=\"$White\"><big><big>Navigation Bar</big></big></font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$LightBlue\">Menu</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$LightBlue\">DB Server</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$LightBlue\">DB Engine</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$LightBlue\">DB User</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$LightBlue\">Database</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$LightBlue\">Table</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$LightBlue\">Records</font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$Black\"><font color=\"$LightBlue\">$NavigationBarMenu</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$LightBlue\">$SelectedHost</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$LightBlue\">$SelectedDBEnv</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$LightBlue\">$AppliedUsername</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$LightBlue\">$SelectedDatabase</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$LightBlue\">$SelectedTable</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$LightBlue\">$SelectedRecords</font></TH>";
  print "  </TR>";
  print "</TABLE>";
  print "<br>\n";

# ------------------------------------------------------------------------------------------------------------------

  print "<TABLE bgcolor=\"$Grey\" width=\"100%\" ALIGN=\"center\" BORDER=\"1\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\" COLSPAN = 6><font color=\"$White\"><big><big>Generic Action Bar</big></big></font></TH>";
  print "  </TR>";
  #print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  #print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  #print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  #print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  #print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  #print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$DarkBlue\"><INPUT NAME=\"Generic_Action_Back\" TYPE=\"submit\" VALUE=\"$GenericActionBackDescription\" $GenericActionBackDisabled></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><INPUT NAME=\"Generic_Action_Add\" TYPE=\"submit\" VALUE=\"$GenericActionAddDescription\" $GenericActionAddDisabled></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><INPUT NAME=\"Generic_Action_Refresh\" TYPE=\"submit\" VALUE=\"$GenericActionRefreshDescription\" $GenericActionRefreshDisabled></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><INPUT NAME=\"Generic_Action_Previous\" TYPE=\"submit\" VALUE=\"$GenericActionPreviousDescription\" $GenericActionPreviousDisabled></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><INPUT NAME=\"Generic_Action_Next\" TYPE=\"submit\" VALUE=\"$GenericActionNextDescription\" $GenericActionNextDisabled></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><INPUT NAME=\"Generic_Action_Email\" TYPE=\"button\" VALUE=\"Email Author\" onClick=\"Email_Author();\"></TH>";
  print "  </TR>";
  print "</TABLE>";
  print "<br>\n";
}

# ==================================================================================================================

sub Initialize_First_Session
{
   if ( $DebugLevel =~ '^True$' )
   {
      print "Started Initialize_First_Session<br>\n";
   }

   if (( -e "$ConfigurationPath/$ConfigurationFile" ) and ( -s "$ConfigurationPath/$ConfigurationFile" ))
   {
      if ( $DebugLevel =~ '^True$' )
      {
         print "Test: $ConfigurationPath/$ConfigurationFile present";
      }

      open(CONFIGFILE,"$ConfigurationPath/$ConfigurationFile") || die('Sorry, could not open ..../$ConfigurationPath/$ConfigurationFile configuration file!');
      $Counted=0;
      while(<CONFIGFILE>)
      {
         if ( ! /^\n|^#/ )
         {
            split(/:/);
            $Counted = (++$Counted);
            $Hosts[$Counted] = $_[0];
            $DBEnv[$Counted] = $_[1];
         }
      }
      close(CONFIGFILE);
      if ($Counted =~ 0)
      {
         if ( $DebugLevel =~ '^True$' )
         {
            print "Test: No configuration lines in $ConfigurationPath/$ConfigurationFile<br>\n";
            print "Action: Turning FirstSessionFlag to: True<br>\n";
            $InitializedFirstSession = 'True';
         }
         open(CONFIGFILE,">$ConfigurationPath/$ConfigurationFile") || die('Sorry, could not open ..../$ConfigurationPath/$ConfigurationFile configuration file!');
         Initialize_First_Session();
      }
   }
   else
   {
      if ( $DebugLevel =~ '^True$' )
      {
         print "Test: $ConfigurationPath/$ConfigurationFile NOT present or 0 Sized<br>\n";
         print "Action: Turning FirstSessionFlag to: True<br>\n";
      }
      open(CONFIGFILE,">$ConfigurationPath/$ConfigurationFile") || die('Sorry, couldn\'t open ..../$ConfigurationPath/$ConfigurationFile configuration file!');
      print CONFIGFILE "localhost:mysql\n";
      close(CONFIGFILE);
      $InitializedFirstSession = 'True';
   }
}

# ==================================================================================================================
# ==================================================================================================================
# ===================================================INPUT BLOCK====================================================
# ==================================================================================================================
# ==================================================================================================================

sub Form_Phase_Selector
{

  if ( $DebugLevel =~ '^True$' )
  {
     print "Started Form_Phase_Selector<br>\n";
     Display_Parameters;
  }

  if ($q->param('Form_Phase'))
  {

# ==================================================================================================================

     if ( $q->param('Form_Phase') =~ '^Hosts_Menu$' )
     {
        if ( $DebugLevel =~ '^True$' )
        {
           print "Form_Phase: Hosts_Menu Detected<br>\n";
        }

        foreach $ParamEntry ($q->param)
        {
           if ($q->param($ParamEntry))
           {

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Add$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Add Detected<br>\n";
                 }
                 Hosts_Menu_Add_Host();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ 'Generic_Action_Refresh')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Refresh Detected<br>\n";
                 }
                 Hosts_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Delete_Host_Button_.*')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Delete_Host_Button Detected<br>\n";
                 }

                 split(/_/,$ParamEntry);
                 $DeleteString = $q->param('Entry_Identifier_'.$_[3]);
                 open(CONFIGFILE,"$ConfigurationPath/$ConfigurationFile");
                 $LoopCounter = 0;
                 while (<CONFIGFILE>)
                 {
                    $CompareString = $_;
                    $_ = $DeleteString;
                    s/\r\n//;
                    $DeleteString = $_;
                    $_ = $CompareString;
                    s/\r\n//;
                    chomp;
                    $CompareString = $_;
                    chomp $CompareString;
                    if ( "$DeleteString" !~ "$CompareString" )
                    {
                       $LoopCounter = (++$LoopCounter);
                       $Lines[$LoopCounter] = $CompareString;
                    }
                 }
                 close(CONFIGFILE);
                 open(CONFIGFILE,">$ConfigurationPath/$ConfigurationFile");
                 foreach $LineEntry (@Lines)
                 {
                    print CONFIGFILE "$LineEntry\n";
                 }
                 close(CONFIGFILE);
                 Hosts_Menu();
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Login_Host_Button_.*')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Login_Host_Button Detected<br>\n";
                 }

                 open(CONFIGFILE,"$ConfigurationPath/$ConfigurationFile") || die('Sorry, couldn\'t open ..../$ConfigurationPath/$ConfigurationFile configuration file!');
                 $Counted=0;
                 while(<CONFIGFILE>)
                 {
                    if ( ! /^\n|^#/ )
                    {
                       split(/:/);
                       $Counted = (++$Counted);
                       $Hosts[$Counted] = $_[0];
                       $DBEnv[$Counted] = $_[1];
                    }
                 }
                 close(CONFIGFILE);

                 $LoopCounter=0;
                 $ValidAction = "false";
                 foreach $HostEntry (@Hosts)
                 {
                    $LoopCounter = (++$LoopCounter);
                    $LoginHostButtonActivated = "false";
                    $UserApplied = "false";
                    $PasswordApplied = "false";
                    if ( $q->param("Login_Host_Button_$LoopCounter")=~ "Login" ) { $LoginHostButtonActivated = "True" }
                    if ( $q->param("Username_$LoopCounter")) { $UserApplied = "True" }
                    if ( $q->param("Password_$LoopCounter")) { $PasswordApplied = "True" }
                    if (($LoginHostButtonActivated =~ "True") and ($UserApplied =~ "True"))
                    {
                       # Well, well, well, we came quite far, This record contains all the required parameters
                       # Set the variable ValidAction to True and as soon as we come out this loop, we can go for the next subroutine
                       # Doesn't that sound like a party

                       $SelectedHost = "${Hosts[$LoopCounter]}";
                       $SelectedDBEnv = "${DBEnv[$LoopCounter]}";
                       chomp($SelectedDBEnv);
                       $AppliedUsername = $q->param("Username_$LoopCounter");
                       $AppliedPassword = $q->param("Password_$LoopCounter");
                       $ValidAction = "True";
                    }
                 }
                 if ( $ValidAction =~ "True" )
                 {
                    Databases_Menu();
                 }

# ------------------------------------------------------------------------------------------------------------------

                 else
                 {
                    # Unfortunately the user activated the button, but we couldn't validate the requirements
                    $LastErrorMessage = 'Last message: Bad Login Attempt. Try again please...';
                    Error_Message();
                    Hosts_Menu();
                 }
              }
           }
        }
     }

# ==================================================================================================================

     if ( $q->param('Form_Phase') =~ '^Hosts_Menu_Add_Host$' )
     {
        if ( $DebugLevel =~ '^True$' )
        {
           print "Form_Phase: Hosts_Menu_Add_Host Detected<br>\n";
        }

        foreach $ParamEntry ($q->param)
        {
           if ($q->param($ParamEntry))
           {

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Back$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Back Detected<br>\n";
                 }
                 Hosts_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Refresh$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Refresh Detected<br>\n";
                 }
                 Hosts_Menu_Add_Host();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Applied_Host_Button$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Applied_Host_Button Detected<br>\n";
                 }
                 if (($q->param('Applied_New_Host')) and ($q->param('Applied_New_DB_Env') !~ 'Select Driver'))
                 {
                    $AppliedNewHost = $q->param('Applied_New_Host');
                    $AppliedNewDBEnv = $q->param('Applied_New_DB_Env');
                    open(CONFIGFILE,">>$ConfigurationPath/$ConfigurationFile");# || die('Sorry, couldn\'t open ..../$ConfigurationPath/$ConfigurationFile configuration file!');
                    print CONFIGFILE "$AppliedNewHost:$AppliedNewDBEnv\n";
                    close(CONFIGFILE);
                    Hosts_Menu();
                 }
              }
           }
        }
     }

# ==================================================================================================================

     if ($q->param('Form_Phase') =~ '^Databases_Menu$')
     {
        $SelectedHost = $q->param('Selected_Host');
        $SelectedDBEnv = $q->param('Selected_DB_Env');
        $AppliedUsername = $q->param('Applied_Username');
        $AppliedPassword = $q->param('Applied_Password');

        if ( $DebugLevel =~ '^True$' )
        {
           print "Form_Phase: Databases_Menu Detected<br>\n";
        }

        foreach $ParamEntry ($q->param)
        {
           if ($q->param($ParamEntry))
           {

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Add$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Add Detected<br>\n";
                 }
                 Databases_Menu_Add_Database();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Back$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Back<br>\n";
                 }
                 Hosts_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Refresh$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Refresh<br>\n";
                 }
                 Databases_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Show_Database_Button_.*')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Show_Database_Button Detected<br>\n";
                 }
                 split(/_/,$ParamEntry);
                 $SelectedDatabase = $q->param('Entry_Identifier_'.$_[3]);
                 Tables_Menu();
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Copy_Database_Button_.*')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Copy_Database_Button Detected<br>\n";
                 }
                 split(/_/,$ParamEntry);
                 $SelectedDatabaseToCopy = $q->param('Entry_Identifier_'.$_[3]);
                 Databases_Menu_Copy_Database();
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Drop_Database_Button_.*')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Drop_Database_Button Detected<br>\n";
                 }
                 split(/_/,$ParamEntry);
                 $DeleteDatabaseString = $q->param('Entry_Identifier_'.$_[3]);
                 $dbh = DBI->connect("dbi\:$SelectedDBEnv\:\:$SelectedHost", "$AppliedUsername", "$AppliedPassword") or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth = $dbh->prepare( "DROP DATABASE $DeleteDatabaseString" ) or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $dbh->disconnect or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 Databases_Menu();
              }
           }
        }
     }

# ==================================================================================================================

     if ( $q->param('Form_Phase') =~ '^Databases_Menu_Add_Database$' )
     {
        if ( $DebugLevel =~ '^True$' )
        {
           print "Form_Phase: Databases_Menu_Add_Database Detected<br>\n";
        }

        $SelectedHost = $q->param('Selected_Host');
        $SelectedDBEnv = $q->param('Selected_DB_Env');
        $AppliedUsername = $q->param('Applied_Username');
        $AppliedPassword = $q->param('Applied_Password');

        foreach $ParamEntry ($q->param)
        {
           if ($q->param($ParamEntry))
           {

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Back$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Back Detected<br>\n";
                 }

                 Databases_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Refresh$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Refresh Detected<br>\n";
                 }
                 Databases_Menu_Add_Database();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Applied_Database_Button$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Applied_Database_Button Detected<br>\n";
                 }

                 if ($q->param('Applied_New_Database'))
                 {
                    $AppliedNewDatabase = $q->param('Applied_New_Database');
                    $CreateDatabaseSQLString = "CREATE DATABASE $AppliedNewDatabase";
                    $dbh = DBI->connect("dbi\:$SelectedDBEnv\:\:$SelectedHost", "$AppliedUsername", "$AppliedPassword") or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    $sth = $dbh->prepare( "$CreateDatabaseSQLString" ) or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message("$CreateDatabaseSQLString $ErrorString");}
                    $dbh->disconnect or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

                    Databases_Menu();
                 }
              }
           }
        }
     }

# ==================================================================================================================

     if ( $q->param('Form_Phase') =~ '^Databases_Menu_Copy_Database$' )
     {
        if ( $DebugLevel =~ '^True$' )
        {
           print "Form_Phase: Databases_Menu_Copy_Database Detected<br>\n";
        }

        $SelectedHost = $q->param('Selected_Host');
        $SelectedDBEnv = $q->param('Selected_DB_Env');
        $AppliedUsername = $q->param('Applied_Username');
        $AppliedPassword = $q->param('Applied_Password');
        $SelectedDatabaseToCopy = $q->param('Applied_Copy_Source_Database');

        foreach $ParamEntry ($q->param)
        {
           if ($q->param($ParamEntry))
           {

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Back$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Back Detected<br>\n";
                 }
                 Databases_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Refresh$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Refresh Detected<br>\n";
                 }
                 Databases_Menu_Copy_Database();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Applied_Copy_Database_Button$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Applied_Copy_Database_Button Detected<br>\n";
                 }
                 $AppliedDatabaseToCopyFrom = $q->param('Applied_Copy_Source_Database');
                 $AppliedDatabaseToCopyTo = $q->param('Applied_Copy_Destination_Database');

                 $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$AppliedDatabaseToCopyFrom\:$SelectedHost",$q->param('Applied_Username'),$q->param('Applied_Password')) or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth = $dbh->prepare( "SHOW TABLES" ) or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

                 $LoopCounter = 0;
                 while ( @TableEntry = $sth->fetchrow_array())
                 {
                    if (@TableEntry)
                    {
                       $Tables[$LoopCounter] = $TableEntry[0];
                       $LoopCounter = (++$LoopCounter);
                    }
                 }
                 $dbh->disconnect or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

                 foreach $TableEntry (@Tables)
                 {
                    $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$AppliedDatabaseToCopyFrom\:$SelectedHost",$q->param('Applied_Username'),$q->param('Applied_Password')) or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    $sth = $dbh->prepare( "CREATE TABLE $AppliedDatabaseToCopyTo.$TableEntry AS SELECT * FROM $AppliedDatabaseToCopyFrom.$TableEntry" ) or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    #print "CREATE TABLE $AppliedDatabaseToCopyTo.$TableEntry AS SELECT * FROM $AppliedDatabaseToCopyFrom.$TableEntry<br>";
                 }
                 $dbh->disconnect or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 Databases_Menu();
              }
           }
        }
     }

# ==================================================================================================================

     if ($q->param('Form_Phase') =~ '^Tables_Menu$')
     {
        if ( $DebugLevel =~ '^True$' )
        {
           print "Form_Phase: Tables_Menu Detected<br>\n";
        }

        $SelectedHost = $q->param('Selected_Host');
        $SelectedDBEnv = $q->param('Selected_DB_Env');
        $SelectedDatabase = $q->param('Selected_Database');
        $AppliedUsername = $q->param('Applied_Username');
        $AppliedPassword = $q->param('Applied_Password');

        foreach $ParamEntry ($q->param)
        {
           if ($q->param($ParamEntry))
           {

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Add$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Add Detected<br>\n";
                 }
                 Tables_Menu_Add_Table();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Back$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Back Detected<br>\n";
                 }
                 Databases_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Refresh$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Refresh Detected<br>\n";
                 }
                 if (( $SelectedDBEnv =~ m/^mysql$/ ) and ( $SelectedDatabase =~ m/^mysql$/ ))
                 {
                    $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost", "$AppliedUsername", "$AppliedPassword") or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    $sth = $dbh->prepare( "FLUSH PRIVILEGES" ) or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    $dbh->disconnect or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 }
                 else
                 {

                 }

                 Tables_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Show_Table_Button_.*')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Show_Table_Button Detected<br>\n";
                 }

                 split(/_/,$ParamEntry);
                 $SelectedTable = $q->param('Entry_Identifier_'.$_[3]);
                 Records_Menu();
              }
# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Drop_Table_Button_.*')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Drop_Table_Button Detected<br>\n";
                 }

                 split(/_/,$ParamEntry);
                 $DeleteTableString = $q->param('Entry_Identifier_'.$_[3]);

                 $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost", "$AppliedUsername", "$AppliedPassword") or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth = $dbh->prepare( "DROP TABLE $DeleteTableString" ) or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $dbh->disconnect or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 Tables_Menu();
              }

           }
        }
     }

# ==================================================================================================================

     if ($q->param('Form_Phase') =~ '^Tables_Menu_Add_Table$')
     {
        if ( $DebugLevel =~ '^True$' )
        {
           print "Form_Phase: Tables_Menu_Add_Menu Detected<br>\n";
        }

        $SelectedHost = $q->param('Selected_Host');
        $SelectedDBEnv = $q->param('Selected_DB_Env');
        $SelectedDatabase = $q->param('Selected_Database');
        $SelectedTable = $q->param('Selected_Table');
        $AppliedUsername = $q->param('Applied_Username');
        $AppliedPassword = $q->param('Applied_Password');

        foreach $ParamEntry ($q->param)
        {
           if ($q->param($ParamEntry))
           {

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Add$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Add Detected<br>\n";
                 }
                    Tables_Menu_Add_Table();
                    exit;

              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Back$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Back Detected<br>\n";
                 }
                 Tables_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Refresh$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Refresh Detected<br>\n";
                 }
                 Tables_Menu_Add_Table();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Create_Table_Button$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Create_Table_Button Detected<br>\n";
                 }
                 if ($q->param('Applied_Table_Name'))
                 {
                    $AppliedTableName = $q->param('Applied_Table_Name');
                    $CreateTableSQLString = 'CREATE TABLE '.$AppliedTableName.' (';
                    $FirstLoop = 'True';
                    $LoopCounter = 0;
                    foreach $ParamEntry ($q->param)
                    {
                       if ($ParamEntry =~ '^Applied_Field_Name_')
                       {
                          split(/_/,$ParamEntry);
                          if ( $DebugLevel =~ '^True$' )
                          {
                             print "Test: Old Applied_Field_Name_$_[3] Records Detected<br>\n";
                          }
                          $AppliedFieldPrimaryKey    = $q->param('Applied_Field_Primary_Key_'.$_[3]);
                          $AppliedFieldName          = $q->param('Applied_Field_Name_'.$_[3]);
                          $AppliedFieldType          = $q->param('Applied_Field_Type_'.$_[3]);
                          $AppliedFieldSize          = $q->param('Applied_Field_Size_'.$_[3]);
                          $AppliedFieldAutoIncrement = $q->param('Applied_Field_Auto_Increment_'.$_[3]);
                          $AppliedFieldAllowedNull   = $q->param('Applied_Field_Allowed_Null_'.$_[3]);
                          if ($AppliedFieldPrimaryKey)
                          {
                             $AppliedFieldPrimaryKey = 'PRIMARY KEY';
                          }
                          else
                          {
                             $AppliedFieldPrimaryKey = '';
                          }
                          $AppliedFieldName = $AppliedFieldName;


                          $DBFieldTypeIsSizeless = 'False';
                          foreach $SizelessDBFieldTypeEntry (@SizelessDBFieldTypes)
                          {
                             if ($SizelessDBFieldTypeEntry =~ $AppliedFieldType)
                             {
                                $DBFieldTypeIsSizeless = 'True';
                             }
                          }
                          if ($DBFieldTypeIsSizeless =~ 'True')
                          {
                             $AppliedFieldType = $AppliedFieldType;
                          }
                          else
                          {
                             $AppliedFieldType .= '('."$AppliedFieldSize".')';
                          }


                          if ($AppliedFieldAutoIncrement)
                          {
                             $AppliedFieldAutoIncrement = 'AUTO_INCREMENT';
                          }
                          else
                          {
                             $AppliedFieldAutoIncrement = '';
                          }
                          if ($AppliedFieldAllowedNull)
                          {
                             $AppliedFieldAllowedNull = 'NULL';
                          }
                          else
                          {
                             $AppliedFieldAllowedNull = 'NOT NULL';
                          }
                          if ($FirstLoop =~ '^True$')
                          {
                             $CreateTableSQLString .= "$AppliedFieldName $AppliedFieldType $AppliedFieldPrimaryKey $AppliedFieldAutoIncrement $AppliedFieldAllowedNull";
                          }
                          else
                          {
                             $CreateTableSQLString .= ", $AppliedFieldName $AppliedFieldType $AppliedFieldPrimaryKey $AppliedFieldAutoIncrement $AppliedFieldAllowedNull";
                          }
                          $FirstLoop = 'False';
                          $LoopCounter = (++$LoopCounter);
                       }
                    }



                    $AppliedFieldName = $q->param('Applied_Field_Name');

                    if ($q->param('Applied_Field_Name'))
                    {
                       if ( $DebugLevel =~ '^True$' )
                       {
                          print "Test: New Applied_Field_Name Record Detected<br>\n";
                       }
                       $AppliedFieldPrimaryKey    = $q->param('Applied_Field_Primary_Key');
                       $AppliedFieldName          = $q->param('Applied_Field_Name');
                       $AppliedFieldType          = $q->param('Applied_Field_Type');
                       $AppliedFieldSize          = $q->param('Applied_Field_Size');
                       $AppliedFieldAutoIncrement = $q->param('Applied_Field_Auto_Increment');
                       $AppliedFieldAllowedNull   = $q->param('Applied_Field_Allowed_Null');

                       if ($AppliedFieldPrimaryKey)
                       {
                          $AppliedFieldPrimaryKey = 'PRIMARY KEY';
                       }
                       else
                       {
                          $AppliedFieldPrimaryKey = '';
                       }

                       $Applied_Field_Name = $Applied_Field_Name;


                       $DBFieldTypeIsSizeless = 'False';
                       foreach $SizelessDBFieldTypeEntry (@SizelessDBFieldTypes)
                       {
                          if ($SizelessDBFieldTypeEntry =~ $AppliedFieldType)
                          {
                             $DBFieldTypeIsSizeless = 'True';
                          }
                       }
                       if ($DBFieldTypeIsSizeless =~ 'True')
                       {
                          $AppliedFieldType = $AppliedFieldType;
                       }
                       else
                       {
                          $AppliedFieldType .= '('."$AppliedFieldSize".')';
                       }


                       if ($AppliedFieldAutoIncrement)
                       {
                          $AppliedFieldIndexed = 'AUTO_INCREMENT';
                       }
                       else
                       {
                          $AppliedFieldAutoIncrement = '';
                       }
                       if ($AppliedFieldAllowedNull)
                       {
                          $AppliedFieldAllowedNull = 'NULL';
                       }
                       else
                       {
                          $AppliedFieldAllowedNull = 'NOT NULL';
                       }
                       if ($FirstLoop =~ '^True$')
                       {
                          $CreateTableSQLString .= "$AppliedFieldName $AppliedFieldType $AppliedFieldPrimaryKey $AppliedFieldAutoIncrement $AppliedFieldAllowedNull";
                       }
                       else
                       {
                          $CreateTableSQLString .= ", $AppliedFieldName $AppliedFieldType $AppliedFieldPrimaryKey $AppliedFieldAutoIncrement $AppliedFieldAllowedNull";
                       }
                    }
                    $CreateTableSQLString .= ')';


                    if ( $DebugLevel =~ '^True$' )
                    {
                       print "Finished Generating: CreateTableSQLString<br>\n";
                       print "$CreateTableSQLString<br>\n";
                    }

                    $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost", "$AppliedUsername", "$AppliedPassword") or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); }
                    $sth = $dbh->prepare( "$CreateTableSQLString" ) or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); }
                    $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message("$CreateTableSQLString $ErrorString"); }
                    $dbh->disconnect or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); }
                    Tables_Menu();
                    exit;
                 }
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Delete_Field_Button_.*')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Delete_Field_Button Detected<br>\n";
                 }
                 split(/_/,$ParamEntry);
                 $SelectedAppliedFieldNameNumber = $_[3];
                 $SelectedAppliedFieldName = $q->param('Applied_Field_Name_'.$SelectedAppliedFieldNameNumber);
                 $OldValueOfSelectedAppliedFieldName = $q->param('Applied_Field_Name_'.$SelectedAppliedFieldNameNumber);
                 $q->param(-Name=>'Applied_Field_Name_'.$SelectedAppliedFieldNameNumber, -Value=>'');
                 $NewValueOfSelectedAppliedFieldName = $q->param('Applied_Field_Name_'.$SelectedAppliedFieldNameNumber);
                 Tables_Menu_Add_Table();
                 exit;
              }
           }
        }
     }

# ==================================================================================================================

     if ($q->param('Form_Phase') =~ /^Records_Menu$/)
     {
        if ( $DebugLevel =~ '^True$' )
        {
           print "Form_Phase: Records_Menu Detected<br>\n";
        }

        $SelectedHost = $q->param('Selected_Host');
        $SelectedDBEnv = $q->param('Selected_DB_Env');
        $SelectedDatabase = $q->param('Selected_Database');
        if ($SelectedTable) { $SelectedTable = $q->param('Selected_Table') };
        $AppliedUsername = $q->param('Applied_Username');
        $AppliedPassword = $q->param('Applied_Password');

        foreach $ParamEntry ($q->param)
        {
           if ($q->param($ParamEntry))
           {
# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Back$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Back Detected<br>\n";
                 }

                 Tables_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Add$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Add Detected<br>\n";
                 }

                 Records_Menu_Add_Record();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Refresh$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Refresh Detected<br>\n";
                 }

                 if (( $SelectedDBEnv =~ m/^mysql$/ ) and ( $SelectedDatabase =~ m/^mysql$/ ))
                 {
                    $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost", "$AppliedUsername", "$AppliedPassword") or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    $sth = $dbh->prepare( "FLUSH PRIVILEGES" ) or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                    $dbh->disconnect or warn $DBI::errstr;
                    $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 }
                 else
                 {

                 }

                 $SelectedTable = $q->param('Selected_Table');
                 Records_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Previous$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Previous Detected<br>\n";
                 }

                 $SelectedTable = $q->param('Selected_Table');
                 Records_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Next$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Next Detected<br>\n";
                 }

                 $SelectedTable = $q->param('Selected_Table');
                 Records_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Edit_Record_Button_.*')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Edit_Record_Button Detected<br>\n";
                 }
                 Records_Menu_Edit_Record();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ m/^Delete_Record_Button_/)
              {
                 $SelectedTable = $q->param('Selected_Table');
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Delete_Record_Button Detected<br>\n";
                 }

                 $DeleteRecordSQLString = "DELETE FROM $SelectedTable WHERE ";

                 foreach $ParamEntry ($q->param)
                 {
                    if ($ParamEntry =~ m/^Delete_Record_Button_/)
                    {
                       $WhereClauseIdentifier = $ParamEntry;
                       $_ = $WhereClauseIdentifier;
                       @IdentifierFieldPairs = split /BeGiN/, $WhereClauseIdentifier;
                       $LoopCounter = 0;
                       foreach $IdentifierFieldPairsEntry (@IdentifierFieldPairs)
                       {
                          if ($IdentifierFieldPairsEntry !~ /^Delete_Record_Button_$/ )
                          {
                             $IdentifierFieldNames[$LoopCounter] = $IdentifierFieldPairsEntry;
                             $_ = $IdentifierFieldNames[$LoopCounter]; s/BeTwEeN.*//; $IdentifierFieldNames[$LoopCounter] = $_;
                             $IdentifierFieldValues[$LoopCounter] = $IdentifierFieldPairsEntry;
                             $_ = $IdentifierFieldValues[$LoopCounter]; s/.*BeTwEeN//; $IdentifierFieldValues[$LoopCounter] = $_;
                             $DeleteRecordSQLString .= "$IdentifierFieldNames[$LoopCounter]=\'$IdentifierFieldValues[$LoopCounter]\' AND ";
                             if ( $DebugLevel =~ /^True$/ )
                             {
                                print "Lifting: $IdentifierFieldNames[$LoopCounter] = $IdentifierFieldValues[$LoopCounter]<br>\n";
                             }
                             $LoopCounter = (++$LoopCounter);
                          }
                       }
                    }
                 }
                 $_ = $DeleteRecordSQLString;
                 s/ AND.$/;/;
                 $DeleteRecordSQLString = $_;
                 print "$DeleteRecordSQLString<br>\n";
                 $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost","$AppliedUsername","$AppliedPassword") or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth = $dbh->prepare("$DeleteRecordSQLString") or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $dbh->disconnect or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

                 Records_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Sort_Column_Button_.*')
              {
                 $SelectedTable = $q->param('Selected_Table');
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Sort_Column_Button Detected<br>\n";
                 }
                 Records_Menu();
                 exit;
              }

           }
        }
     }

# ==================================================================================================================

     if ($q->param('Form_Phase') =~ '^Records_Menu_Add_Record$')
     {
        if ( $DebugLevel =~ '^True$' )
        {
           print "Form_Phase: Records_Menu_Add_Record Detected<br>\n";
        }

        $SelectedHost = $q->param('Selected_Host');
        $SelectedDBEnv = $q->param('Selected_DB_Env');
        $SelectedDatabase = $q->param('Selected_Database');
        $SelectedTable = $q->param('Selected_Table');
        $AppliedUsername = $q->param('Applied_Username');
        $AppliedPassword = $q->param('Applied_Password');

        foreach $ParamEntry ($q->param)
        {
           if ($q->param($ParamEntry))
           {
# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Back$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Back Detected<br>\n";
                 }

                 Records_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Refresh$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Refresh Detected<br>\n";
                 }

                 $SelectedTable = $q->param('Selected_Table');
                 Records_Menu_Add_Record();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Insert_Record_Button$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Insert_Record_Button Detected<br>\n";
                 }
                 $InsertRecordSQLString = 'INSERT INTO '.$SelectedTable.' SET ';

                 $LoopCounter = 0;
                 foreach $ParamEntry ($q->param)
                 {
                    if ($ParamEntry =~ m/^Applied_Insert_Record_Field_/)
                    {
                       $_ = $ParamEntry;
                       s/^Applied_Insert_Record_Field_//;
                       $InsertRecordFieldNames[$LoopCounter] = $_;
                       $InsertRecordFieldValues[$LoopCounter] = $q->param("Applied_Insert_Record_Field_$InsertRecordFieldNames[$LoopCounter]");
                       $LoopCounter = (++$LoopCounter);
                    }
                 }

                 $LoopCounter = 0;
                 foreach $InsertRecordFieldNamesEntry (@InsertRecordFieldNames)
                 {
                    $InsertRecordSQLString .= $InsertRecordFieldNamesEntry."=\'".$InsertRecordFieldValues[$LoopCounter]."\', ";
                    $LoopCounter = (++$LoopCounter);
                 }
                 $_ = $InsertRecordSQLString;
                 chomp;
                 s/,.$/;/;
                 $InsertRecordSQLString = $_;
                 print "$InsertRecordSQLString<br>\n";

                 $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost","$AppliedUsername","$AppliedPassword") or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth = $dbh->prepare("$InsertRecordSQLString") or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $dbh->disconnect or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

                 Records_Menu();
                 exit;
              }
           }
        }
     }

# ==================================================================================================================

     if ($q->param('Form_Phase') =~ '^Records_Menu_Edit_Record$')
     {
        if ( $DebugLevel =~ '^True$' )
        {
           print "Form_Phase: Records_Menu_Edit_Record Detected<br>\n";
        }

        $SelectedHost = $q->param('Selected_Host');
        $SelectedDBEnv = $q->param('Selected_DB_Env');
        $SelectedDatabase = $q->param('Selected_Database');
        $SelectedTable = $q->param('Selected_Table');
        $AppliedUsername = $q->param('Applied_Username');
        $AppliedPassword = $q->param('Applied_Password');

        foreach $ParamEntry ($q->param)
        {
           if ($q->param($ParamEntry))
           {
# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Back$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Back Detected<br>\n";
                 }

                 Records_Menu();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ '^Generic_Action_Refresh$')
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Generic_Action_Refresh Detected<br>\n";
                 }

                 $SelectedTable = $q->param('Selected_Table');
                 Records_Menu_Edit_Record();
                 exit;
              }

# ------------------------------------------------------------------------------------------------------------------

              if ($ParamEntry =~ m/^Update_Record_Button_/)
              {
                 if ( $DebugLevel =~ '^True$' )
                 {
                    print "Action: Update_Record_Button Detected<br>\n";
                 }


                 $UpdateRecordSQLString = "UPDATE $SelectedTable SET ";
                 $LoopCounter = 0;
                 foreach $ParamEntry ($q->param)
                 {
                    if ($ParamEntry =~ m/^Applied_Update_Record_Field_/)
                    {
                       $_ = $ParamEntry;
                       s/^Applied_Update_Record_Field_//;
                       $UpdateRecordFieldNames[$LoopCounter] = $_;
                       $UpdateRecordFieldValues[$LoopCounter] = $q->param("Applied_Update_Record_Field_$UpdateRecordFieldNames[$LoopCounter]");
                       $LoopCounter = (++$LoopCounter);
                    }
                 }

                 $LoopCounter = 0;
                 foreach $UpdateRecordFieldNamesEntry (@UpdateRecordFieldNames)
                 {
                    $UpdateRecordSQLString .= $UpdateRecordFieldNamesEntry."=\'".$UpdateRecordFieldValues[$LoopCounter]."\', ";
                    $LoopCounter = (++$LoopCounter);
                 }
                 $_ = $UpdateRecordSQLString;
                 chomp;
                 s/,.$//;
                 $UpdateRecordSQLString = $_;
                 $UpdateRecordSQLString .= " WHERE ";


                 foreach $ParamEntry ($q->param)
                 {
                    if ($ParamEntry =~ m/^Update_Record_Button_/)
                    {
                       $WhereClauseIdentifier = $ParamEntry;
                       $_ = $WhereClauseIdentifier;
                       @IdentifierFieldPairs = split /BeGiN/, $WhereClauseIdentifier;
                       $LoopCounter = 0;
                       foreach $IdentifierFieldPairsEntry (@IdentifierFieldPairs)
                       {
                          if ($IdentifierFieldPairsEntry !~ /^Update_Record_Button_Edit_Record_Button_$/ )
                          {
                             $IdentifierFieldNames[$LoopCounter] = $IdentifierFieldPairsEntry;
                             $_ = $IdentifierFieldNames[$LoopCounter]; s/BeTwEeN.*//; $IdentifierFieldNames[$LoopCounter] = $_;
                             $IdentifierFieldValues[$LoopCounter] = $IdentifierFieldPairsEntry;
                             $_ = $IdentifierFieldValues[$LoopCounter]; s/.*BeTwEeN//; $IdentifierFieldValues[$LoopCounter] = $_;
                             $UpdateRecordSQLString .= "$IdentifierFieldNames[$LoopCounter]=\'$IdentifierFieldValues[$LoopCounter]\' AND ";
                             if ( $DebugLevel =~ /^True$/ )
                             {
                                print "Lifting: $IdentifierFieldNames[$LoopCounter] = $IdentifierFieldValues[$LoopCounter]<br>\n";
                             }
                             $LoopCounter = (++$LoopCounter);
                          }
                       }
                    }
                 }
                 $_ = $UpdateRecordSQLString;
                 s/ AND.$/;/;
                 $UpdateRecordSQLString = $_;
                 $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost","$AppliedUsername","$AppliedPassword") or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth = $dbh->prepare("$UpdateRecordSQLString") or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $sth->execute  or warn $DBI::errstr; # Oh, tough luck
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 $dbh->disconnect or warn $DBI::errstr;
                 $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
                 Records_Menu();
                 exit;
              }
           }
        }
     }

# ==================================================================================================================

  }
  else
  {
     # No parameters detected, jump to the Hosts_Menu
     if ( $DebugLevel =~ '^True$' )
     {
        print "Form_Phase Detected new session<br>\n";
     }
     Initialize_First_Session();
     Hosts_Menu();
  }
}

# ==================================================================================================================
# ==================================================================================================================
# ===================================================OUTPUT BLOCK===================================================
# ==================================================================================================================
# ==================================================================================================================

sub Hosts_Menu()
{
  if ( $DebugLevel =~ '^True$' )
  {
     print "Form_Phase: Hosts_Menu Started<br>\n";
  }

  $NavigationBarMenu = 'Hosts_Menu';
  $SelectedHost = '';
  $SelectedDBEnv = '';
  $SelectedDatabase = '';
  $SelectedTable = '';
  $AppliedUsername = '';
  $AppliedPassword = '';

  $GenericActionBackDescription = 'Exit';
  $GenericActionBackDisabled = '';
  $GenericActionAddDescription = 'Add Host';
  $GenericActionAddDisabled = '';
  $GenericActionRefreshDescription = 'Refresh';
  $GenericActionRefreshDisabled = '';
  $GenericActionPreviousDescription = 'Previous Page';
  $GenericActionPreviousDisabled = 'DISABLED';
  $GenericActionNextDescription = 'Next Page';
  $GenericActionNextDisabled = 'DISABLED';

  Initialize_First_Session();

  # Reads the configuration file and puts all filtered and valid entries in 2 arrayed variables

  open(CONFIGFILE,"$ConfigurationPath/$ConfigurationFile") || die('Sorry, could not open ..../$ConfigurationPath/$ConfigurationFile configuration file!');
  $Counted=0;
  while(<CONFIGFILE>)
  {
     if ( ! /^\n|^#/ )
     {
        split(/:/);
        $Counted = (++$Counted);
        $Hosts[$Counted] = $_[0];
        $DBEnv[$Counted] = $_[1];
     }
  }
  close(CONFIGFILE);

# ------------------------------------------------------------------------------------------------------------------

  print "<FORM NAME=\"Generic_Form\" METHOD=\"POST\">";
  print "<INPUT TYPE=\"hidden\" NAME=\"Form_Phase\" VALUE=\"Hosts_Menu\">";
  Display_Navigation_Bar();

  print "<TABLE width=\"100%\" ALIGN=\"center\" BORDER=\"2\" bgcolor=\"$Grey\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor = \"$SoftBlue\"COLSPAN = 8><font color=\"$White\"><big><big>$NavigationBarMenu</big></big></font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Num</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">Host</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">Type</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">DB User</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">Password</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Red\">Action</font></TH>";
  print "  </TR>";

# ------------------------------------------------------------------------------------------------------------------

  $LoopCounter=0;
  foreach $HostEntry (@Hosts)
  {
    $LoopCounter = (++$LoopCounter);
    if ( ($Hosts[$LoopCounter]) and ($DBEnv[$LoopCounter]))
    {
      print "  <TR bgcolor=\"$Grey\" ALIGN=\"center\" VALIGN=\"center\">";
      print "    <TH bgcolor=\"$OrangeGrey\"> $LoopCounter</TH>";
      print "    <TH bgcolor=\"$Grey\"><font color=\"$black\">$Hosts[$LoopCounter]</font></TH>";
      print "    <TH bgcolor=\"$Grey\"><font color=\"$black\">$DBEnv[$LoopCounter]</font></TH>";
      print "    <TH><INPUT TYPE=\"text\" NAME=\"Username_$LoopCounter\" SIZE=\"15\" MAXLENGTH=15></TH>";
      print "    <TH><INPUT TYPE=\"password\" NAME=\"Password_$LoopCounter\" VALUE=\"\" SIZE=\"15\" MAXLENGTH=15></TH>";

      if ( $DisableLogin =~ '^True$' )
      {
         print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Login_Host_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Login Disabled\" DISABLED> </TH>";
      }
      else
      {
         print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Login_Host_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Login $MenuElement\"> </TH>";
      }


      print "    <TH bgcolor=\"$RedGrey\"><INPUT NAME=\"Delete_Host_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Delete $MenuElement\" onClick=\"DoConfirm('WARNING\\n\\nYou are about to delete host $Hosts[$LoopCounter].\\n\\nDo you want to continue?')\"></TH>";
#      print "    <TH><INPUT TYPE=\"image\" NAME=\"HostButton$LoopCounter\" SRC=\"/images/NeutralButtonOff.gif\" ALIGN=DOWN></TH>";
      print "  </TR>";
      print "    <TH><INPUT NAME=\"Entry_Identifier_$LoopCounter\" TYPE=\"hidden\" VALUE=\"$Hosts[$LoopCounter]:$DBEnv[$LoopCounter]\"></TH>";
    }
  }
  print "  </TR>";
  print "</TABLE>";
  print "</FORM>";
     Generic_Message($InitializedFirstSessionMessage);
  if ($InitializedFirstSession =~ m/^True$/)
  {
     Error_Message($InitializedFirstSessionMessage);
  }
}

# ==================================================================================================================

sub Hosts_Menu_Add_Host
{
  if ( $DebugLevel =~ '^True$' )
  {
     print "Form_Phase: Hosts_Menu_Add_Host Started<br>\n";
  }

  $NavigationBarMenu = 'Hosts_Menu_Add_Host';
  $SelectedHost = '';
  $SelectedDBEnv = '';
  $SelectedDatabase = '';
  $SelectedTable = '';
  $AppliedUsername = '';
  $AppliedPassword = '';

  $GenericActionAddDescription = 'Disabled';
  $GenericActionAddDisabled = 'DISABLED';
  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionRefreshDescription = 'Refresh';
  $GenericActionRefreshDisabled = '';

  print "<FORM NAME=\"Generic_Form\" METHOD=\"POST\">";
  print "<INPUT TYPE=\"hidden\" NAME=\"Form_Phase\" VALUE=\"Hosts_Menu_Add_Host\">";
  Display_Navigation_Bar();
  print "<TABLE width=\"100%\" ALIGN=\"center\" bgcolor=\"$Grey\" BORDER=\"2\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\" bgcolor=\"$DarkBlue\">";
  print "    <TH bgcolor=\"$SoftBlue\" COLSPAN=10><font color=\"$White\"><big><big>$NavigationBarMenu</big></big></font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\" bgcolor=\"$DarkBlue\">";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Host</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Database Type</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH><INPUT TYPE=\"text\" NAME=\"Applied_New_Host\" SIZE=80></TH>";
  print "    <TH SIZE=30>\n";
  print "      <SELECT NAME=\"Applied_New_DB_Env\" SIZE=1>";
  print "        <OPTION>Select Driver</OPTION>";
  @Drivers = DBI->available_drivers;
  foreach $Driver (@Drivers)
  {
     print "       <OPTION>$Driver</OPTION>";
  }
  print "      </SELECT>";
  print "    </TH>\n";
  print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Applied_Host_Button\" TYPE=\"Submit\" VALUE=\"Add Host\"></TH>";
  print "  </TR>";
}

# ==================================================================================================================

sub Databases_Menu
{
  if ( $DebugLevel =~ '^True$' )
  {
     print "Form_Phase: Databases_Menu Started<br>\n";
  }

  $NavigationBarMenu = 'Databases_Menu';
# $SelectedHost = '';
# $SelectedDBEnv = '';
  $SelectedDatabase = '';
  $SelectedTable = '';
# $AppliedUsername = '';
# $AppliedPassword = '';

  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionAddDescription = 'Add Database';
  $GenericActionAddDisabled = '';
  $GenericActionRefreshDescription = 'Refresh';
  $GenericActionRefreshDisabled = '';
  $GenericActionPreviousDescription = 'Previous Page';
  $GenericActionPreviousDisabled = 'DISABLED';
  $GenericActionNextDescription = 'Next Page';
  $GenericActionNextDisabled = 'DISABLED';

  $dbh = DBI->connect("dbi\:$SelectedDBEnv\:\:$SelectedHost", "$AppliedUsername", "$AppliedPassword") or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); Hosts_Menu();}
  $sth = $dbh->prepare( "SHOW DATABASES" ) or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); Hosts_Menu();}
  $sth->execute or warn $DBI::errstr; # Oh, tough luck
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); Hosts_Menu();}

  $LoopCounter = 0;
  while ( @DatabaseEntry = $sth->fetchrow_array())
  {
     if ($DatabaseEntry[0])
     {
        $Databases[$LoopCounter] = $DatabaseEntry[0];
        $LoopCounter = (++$LoopCounter);
     }
  }
  $dbh->disconnect or warn $DBI::errstr;


# ------------------------------------------------------------------------------------------------------------------

  print "<FORM NAME=\"Generic_Form\" METHOD=\"POST\">";

  print "<INPUT TYPE=\"hidden\" NAME=\"Form_Phase\" VALUE=\"Databases_Menu\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Host\" VALUE=\"$SelectedHost\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_DB_Env\" VALUE=\"$SelectedDBEnv\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Username\" VALUE=\"$AppliedUsername\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Password\" VALUE=\"$AppliedPassword\">\n";

  Display_Navigation_Bar();

  print "<TABLE  width=\"100%\" ALIGN=\"center\" BORDER=\"1\" bgcolor=\"$Grey\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\" bgcolor=\"$DarkBlue\">";
  print "    <TH bgcolor=\"$SoftBlue\" COLSPAN=6><font color=\"$White\"><big><big>$NavigationBarMenu</big></big></font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\" bgcolor=\"$DarkBlue\">";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Num</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">Database</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">Tables</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Red\">Action</font></TH>";
  print "  </TR>";

  $LoopCounter = 0;
  foreach $DatabaseEntry (@Databases)
  {
     $_ = $DatabaseEntry;
     chomp;
     $DatabaseEntry = $_;
     if ($DatabaseEntry)
     {
         $TableCounter = 0;
         $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$DatabaseEntry\:$SelectedHost", "$AppliedUsername", "$AppliedPassword") or warn $DBI::errstr;
         $ErrorString = $DBI::errstr; if ($ErrorString) { Generic_Message($ErrorString); next;}
         $sth = $dbh->prepare( "SHOW TABLES" ) or warn $DBI::errstr;
         $ErrorString = $DBI::errstr; if ($ErrorString) { Generic_Message($ErrorString);}
         $sth->execute or warn $DBI::errstr; # Oh, tough luck
         $ErrorString = $DBI::errstr; if ($ErrorString) { Generic_Message($ErrorString);}
         while ( @Tables = $sth->fetchrow_array())
         {
            if (@Tables)
            {
               $TableCounter = (++$TableCounter);
            }
         }
         $dbh->disconnect or warn $DBI::errstr;
         $ErrorString = $DBI::errstr; if ($ErrorString) { Generic_Message($ErrorString);}

         print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
         print "    <TH bgcolor=\"$OrangeGrey\">$LoopCounter</TH>";
         print "    <TH>$DatabaseEntry</TH>";
         print "    <TH>$TableCounter</TH>";
         print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Show_Database_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Show Database\"></TH>";
         print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Copy_Database_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Copy Database\"></TH>";
         print "    <TH bgcolor=\"$RedGrey\"><INPUT NAME=\"Drop_Database_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Drop Database\" onClick=\"DoConfirm('WARNING\\n\\nYou are about to drop Database $DatabaseEntry.\\n\\nDo you want to continue?')\"></TH>";
         print "    <TH><INPUT NAME=\"Entry_Identifier_$LoopCounter\" TYPE=\"hidden\" VALUE=\"$DatabaseEntry\"></TH>";
         print "  </TR>";
         $LoopCounter = (++$LoopCounter);
     }
  }
  print "</TABLE>";
  print "</FORM>";
}

# ==================================================================================================================

sub Databases_Menu_Add_Database
{
  if ( $DebugLevel =~ '^True$' )
  {
     print "Form_Phase: Databases_Menu_Add_Database Started<br>\n";
  }

  $NavigationBarMenu = 'Databases_Menu_Add_Database';
# $SelectedHost = '';
# $SelectedDBEnv = '';
  $SelectedDatabase = '';
  $SelectedTable = '';
# $AppliedUsername = '';
# $AppliedPassword = '';

  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionAddDescription = 'Disabled';
  $GenericActionAddDisabled = 'DISABLED';
  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionRefreshDescription = 'Refresh';
  $GenericActionRefreshDisabled = '';
  $GenericActionPreviousDescription = 'Previous Page';
  $GenericActionPreviousDisabled = 'DISABLED';
  $GenericActionNextDescription = 'Next Page';
  $GenericActionNextDisabled = 'DISABLED';

  $SelectedHost = $q->param('Selected_Host');
  $SelectedDBEnv = $q->param('Selected_DB_Env');
  $AppliedUsername = $q->param('Applied_Username');
  $AppliedPassword = $q->param('Applied_Password');

  print "<FORM NAME=\"Generic_Form\" METHOD=\"POST\">";
  print "<INPUT TYPE=\"hidden\" NAME=\"Form_Phase\" VALUE=\"Databases_Menu_Add_Database\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Host\" VALUE=\"$SelectedHost\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_DB_Env\" VALUE=\"$SelectedDBEnv\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Username\" VALUE=\"$AppliedUsername\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Password\" VALUE=\"$AppliedPassword\">\n";

  Display_Navigation_Bar();

  print "<TABLE WIDTH=\"100%\" ALIGN=\"center\" BORDER=\"2\" bgcolor=\"$Grey\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\" bgcolor=\"$DarkBlue\">";
  print "    <TH bgcolor=\"$SoftBlue\" COLSPAN = 10><font color=\"$White\"><big><big>$NavigationBarMenu</big></big></font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Database</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH><INPUT TYPE=\"text\" NAME=\"Applied_New_Database\" SIZE=90></TH>";
  print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Applied_Database_Button\" TYPE=\"Submit\" VALUE=\"Add Database\"></TH>";
  print "  </TR>";
  print "</TABLE>";
  print "</FORM>";
}

# ==================================================================================================================

sub Databases_Menu_Copy_Database
{
  if ( $DebugLevel =~ '^True$' )
  {
     print "Form_Phase: Databases_Menu_Copy_Database Started<br>\n";
  }

  $NavigationBarMenu = 'Databases_Menu_Copy_Database';
# $SelectedHost = '';
# $SelectedDBEnv = '';
#  $SelectedDatabase = '';
  $SelectedTable = '';
# $AppliedUsername = '';
# $AppliedPassword = '';

  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionAddDescription = 'Disabled';
  $GenericActionAddDisabled = 'DISABLED';
  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionRefreshDescription = 'Refresh';
  $GenericActionRefreshDisabled = '';
  $GenericActionPreviousDescription = 'Previous Page';
  $GenericActionPreviousDisabled = 'DISABLED';
  $GenericActionNextDescription = 'Next Page';
  $GenericActionNextDisabled = 'DISABLED';

  $dbh = DBI->connect("dbi\:$SelectedDBEnv\:\:$SelectedHost", "$AppliedUsername", "$AppliedPassword") or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth = $dbh->prepare( "SHOW DATABASES" ) or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth->execute  or warn $DBI::errstr; # Oh, tough luck
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

  $LoopCounter = 0;
  while ( @DatabaseEntry = $sth->fetchrow_array())
  {
     if (@DatabaseEntry)
     {
        $Databases[$LoopCounter] = $DatabaseEntry[0];
        $LoopCounter = (++$LoopCounter);
     }
  }
  $dbh->disconnect or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

  print "<FORM NAME=\"Generic_Form\" METHOD=\"POST\">";

  print "<INPUT TYPE=\"hidden\" NAME=\"Form_Phase\" VALUE=\"Databases_Menu_Copy_Database\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Host\" VALUE=\"$SelectedHost\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_DB_Env\" VALUE=\"$SelectedDBEnv\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Username\" VALUE=\"$AppliedUsername\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Password\" VALUE=\"$AppliedPassword\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Copy_Source_Database\" VALUE=\"$SelectedDatabaseToCopy\">\n";

  Display_Navigation_Bar();

  print "<TABLE width=\"100%\" ALIGN=\"center\" BORDER=\"2\" bgcolor=\"$Grey\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\" COLSPAN=10><font color=\"$White\"><big><big>$NavigationBarMenu</big></big></font></TH>";
  print "  </TR>";

  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Source Database</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Red\">Destination Database</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  print "  </TR>";

  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Applied_Copy_Source_Database\" TYPE=\"text\" VALUE=\"$SelectedDatabaseToCopy\" DISABLED></TH>";
  print "    <TH bgcolor=\"$RedGrey\">";
  print "      <SELECT NAME=\"Applied_Copy_Destination_Database\" SIZE=1>";
  print "        <OPTION>Select Database</OPTION>";
  foreach $DatabaseEntry (@Databases)
  {
     print "     <OPTION>$DatabaseEntry</OPTION>";
  }
  print "      </SELECT>";
  print "    </TH>\n";
  print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Applied_Copy_Database_Button\" TYPE=\"Submit\" VALUE=\"Copy Database\" onClick=\"DoConfirm('WARNING\\n\\nYou are about to copy a Database.\\n\\nDo you want to continue?')\"></TH>";
  print "  </TR>";
  print "</TABLE>";
  print "</FORM>";
}

# ==================================================================================================================

sub Tables_Menu
{
  if ( $DebugLevel =~ '^True$' )
  {
     print "Form_Phase: Tables_Menu Started<br>\n";
  }

  $NavigationBarMenu = 'Tables_Menu';
# $SelectedHost = '';
# $SelectedDBEnv = '';
# $SelectedDatabase = '';
  $SelectedTable = '';
# $AppliedUsername = '';
# $AppliedPassword = '';

  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionAddDescription = 'Add Table';
  $GenericActionAddDisabled = '';
  if (( $SelectedDBEnv =~ m/^mysql$/ ) and ( $SelectedDatabase =~ m/^mysql$/ )) { $GenericActionRefreshDescription = 'Refresh (Privileges)'; }
  else { $GenericActionRefreshDescription = 'Refresh'; }
  $GenericActionRefreshDisabled = '';
  $GenericActionPreviousDescription = 'Previous Page';
  $GenericActionPreviousDisabled = 'DISABLED';
  $GenericActionNextDescription = 'Next Page';
  $GenericActionNextDisabled = 'DISABLED';

  $SelectedHost = $q->param('Selected_Host');
  $SelectedDBEnv = $q->param('Selected_DB_Env');
  $AppliedUsername = $q->param('Applied_Username');
  $AppliedPassword = $q->param('Applied_Password');

  $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost",$q->param('Applied_Username'),$q->param('Applied_Password')) or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth = $dbh->prepare( "SHOW TABLES" ) or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth->execute  or warn $DBI::errstr; # Oh, tough luck
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

  $LoopCounter = 0;
  while ( @TableEntry = $sth->fetchrow_array())
  {
     if (@TableEntry)
     {
        $Tables[$LoopCounter] = $TableEntry[0];
        $LoopCounter = (++$LoopCounter);
     }
  }
  #$dbh->disconnect or warn $DBI::errstr;

  $LoopCounter = 0;
  foreach $TableEntry (@Tables)
  {
     if ($TableEntry)
     {
        #$dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost",$q->param('Applied_Username'),$q->param('Applied_Password')) or warn $DBI::errstr;
        $sth = $dbh->prepare( "DESCRIBE $TableEntry" ) or warn $DBI::errstr;
        $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); $LoopCounter = (++$LoopCounter); next;}
        $sth->execute  or warn $DBI::errstr; # Oh, tough luck
        $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); $LoopCounter = (++$LoopCounter); next;}

        $FieldNameCounter = 0;
        while ( @FieldNames = $sth->fetchrow_array())
        {
           $FieldNameCounter = (++$FieldNameCounter);
        }
        $FieldCountEntry[$LoopCounter] = $FieldNameCounter;
        $LoopCounter = (++$LoopCounter);
     }
  }

  $LoopCounter = 0;
  foreach $TableEntry (@Tables)
  {
     if ($Tables[0])
     {
        #$dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost",$q->param('Applied_Username'),$q->param('Applied_Password')) or warn $DBI::errstr;
        $sth = $dbh->prepare( "SELECT COUNT(*) FROM $TableEntry" ) or warn $DBI::errstr;
        $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); $LoopCounter = (++$LoopCounter);next;}
        $sth->execute  or warn $DBI::errstr; # Oh, tough luck
        $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); $LoopCounter = (++$LoopCounter);next;}
        $RecordCountEntry[$LoopCounter] = $sth->fetchrow_array();
        $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString); $LoopCounter = (++$LoopCounter);next;}
        $LoopCounter = (++$LoopCounter);
     }
  }
  $dbh->disconnect or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

# ------------------------------------------------------------------------------------------------------------------

  print "<FORM NAME=\"Generic_Form\" METHOD=\"POST\">";

  print "<INPUT TYPE=\"hidden\" NAME=\"Form_Phase\"    VALUE=\"Tables_Menu\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Host\"    VALUE=\"",$q->param('Selected_Host'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_DB_Env\"  VALUE=\"",$q->param('Selected_DB_Env'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Username\" VALUE=\"",$q->param('Applied_Username'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Password\" VALUE=\"",$q->param('Applied_Password'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Database\"  VALUE=\"$SelectedDatabase\">\n";

  Display_Navigation_Bar();

  print "<TABLE width=\"100%\" ALIGN=\"center\" BORDER=\"1\" bgcolor=\"$Grey\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\" bgcolor=\"$DarkBlue\">";
  print "    <TH bgcolor=\"$SoftBlue\" COLSPAN = 8><font color=\"$White\"><big><big>$NavigationBarMenu</big></big></font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\" bgcolor=\"$DarkBlue\">";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Num</font></TH>";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">Table</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Grey\">Fields</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Grey\">Records</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
##  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
##  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Action</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Red\">Action</font></TH>";
  print "  </TR>";

  $LoopCounter = 0;
  foreach $TableEntry (@Tables)
  {
     if ($TableEntry)
     {
         print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
         print "    <TH bgcolor=\"$OrangeGrey\">$LoopCounter</TH>";
         print "    <TH>$TableEntry</TH>";
         print "    <TH><FONT COLOR=\"$DarkGrey\">$FieldCountEntry[$LoopCounter]</FONT></TH>";
         print "    <TH><FONT COLOR=\"$DarkGrey\">$RecordCountEntry[$LoopCounter]</FONT></TH>";
         print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Show_Table_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Show Table\"></TH>";
##         print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Copy_Table_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Copy Table\"></TH>";
##         print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Alter_Table_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Alter Table\"></TH>";
         print "    <TH bgcolor=\"$RedGrey\"><INPUT NAME=\"Drop_Table_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Drop Table\" onClick=\"DoConfirm('WARNING\\n\\nYou are about to drop Table $TableEntry.\\n\\nDo you want to continue?')\"></TH>";
         print "    <TH><INPUT NAME=\"Entry_Identifier_$LoopCounter\" TYPE=\"hidden\" VALUE=\"$TableEntry\"></TH>";
         print "  </TR>";
         $LoopCounter = (++$LoopCounter);
     }
  }
  print "</TABLE>";
  print "</FORM>";
}

# ==================================================================================================================

sub Tables_Menu_Add_Table
{
  if ( $DebugLevel =~ '^True$' )
  {
     print "Form_Phase: Tables_Menu_Add_Tables Started<br>\n";
  }

  $NavigationBarMenu = 'Hosts_Menu_Add_Table';
# $SelectedHost = '';
# $SelectedDBEnv = '';
# $SelectedDatabase = '';
  $SelectedTable = '';
# $AppliedUsername = '';
# $AppliedPassword = '';

  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionAddDescription = 'Add Field';
  $GenericActionAddDisabled = '';
  $GenericActionRefreshDescription = 'Refresh';
  $GenericActionRefreshDisabled = '';
  $GenericActionPreviousDescription = 'Previous Page';
  $GenericActionPreviousDisabled = 'DISABLED';
  $GenericActionNextDescription = 'Next Page';
  $GenericActionNextDisabled = 'DISABLED';
  $Applied_Table_Name = $q->param('Applied_Table_Name');

# ------------------------------------------------------------------------------------------------------------------

  print "<FORM NAME=\"Generic_Form\" METHOD=\"POST\">";

  print "<INPUT TYPE=\"hidden\" NAME=\"Form_Phase\" VALUE=\"Tables_Menu_Add_Table\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Host\" VALUE=\"$SelectedHost\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_DB_Env\" VALUE=\"$SelectedDBEnv\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Database\" VALUE=\"$SelectedDatabase\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Username\" VALUE=\"$AppliedUsername\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Password\" VALUE=\"$AppliedPassword\">\n";

  Display_Navigation_Bar();

  print "<TABLE width=\"100%\" ALIGN=\"center\" BORDER=\"2\" bgcolor=\"$Grey\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\" COLSPAN=20><font color=\"$White\"><big><big>Add Table Menu</big></big></font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$Black\" COLSPAN=6><font color=\"$Orange\">Table</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH COLSPAN = 6><INPUT TYPE=\"text\" NAME=\"Applied_Table_Name\" VALUE=\"$Applied_Table_Name\" SIZE=90></TH>";
  print "    <TH bgcolor=\"$GreenGrey\"><INPUT NAME=\"Create_Table_Button\" TYPE=\"Submit\" VALUE=\"Create Table\"onClick=\"DoConfirm('WARNING\\n\\nYou are about to apply your table definition including the fields definition as you see them.\\n\\nDo you want to continue?')\"></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\" bgcolor=\"$DarkBlue\">";
  print "    <TH bgcolor = \"$SoftBlue\" COLSPAN = 20><font color=\"$White\"><big><big>Field Definitions</big></big></font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Key</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Name</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Type</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Green\">Size</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Auto</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Null</font></TH>";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Red\">Action</font></TH>";
  print "  </TR>";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "  </TR>";

# ------------------------------------------------------------------------------------------------------------------

  $LoopCounter = 0;
  foreach $ParamEntry ($q->param)
  {
     if ($ParamEntry =~ '^Applied_Field_Name_')
     {
        split(/_/,$ParamEntry);
        if ( $DebugLevel =~ '^True$' )
        {
           print "Test: Old Applied_Field_Name_$_[3] Records Detected<br>\n";
        }

        $AppliedFieldPrimaryKey    = $q->param('Applied_Field_Primary_Key_'.$_[3]);
        $AppliedFieldName          = $q->param('Applied_Field_Name_'.$_[3]);
        $AppliedFieldType          = $q->param('Applied_Field_Type_'.$_[3]);
        $AppliedFieldSize          = $q->param('Applied_Field_Size_'.$_[3]);
        $AppliedFieldAutoIncrement = $q->param('Applied_Field_Auto_Increment_'.$_[3]);
        $AppliedFieldAllowedNull   = $q->param('Applied_Field_Allowed_Null_'.$_[3]);

        if ($AppliedFieldName)
        {
           print "  <TR ALIGN=\"center\" VALIGN=\"center\">";

           if ($AppliedFieldPrimaryKey)
           {
              print "    <TH><INPUT NAME=\"Applied_Field_Primary_Key_$_[3]\" TYPE=\"checkbox\" VALUE=\"CHECKED\" CHECKED></TH>";
           }
           else
           {
              print "    <TH><INPUT NAME=\"Applied_Field_Primary_Key_$_[3]\" TYPE=\"checkbox\" VALUE=\"UNCHECKED\"></TH>";
           }
              print "    <TH><INPUT NAME=\"Applied_Field_Name_$_[3]\" TYPE=\"text\" VALUE=\"$AppliedFieldName\" SIZE=55></TH>";
           print "    <TH>\n";
           print "      <SELECT NAME=\"Applied_Field_Type_$_[3]\" SIZE=1>";

           foreach $DBFieldTypeEntry (@DBFieldTypes)
           {
              if ( $DBFieldTypeEntry =~ /^$AppliedFieldType$/ )
              {
                 print "<OPTION SELECTED>$DBFieldTypeEntry</OPTION>";
              }
              else
              {
                 print "<OPTION>$DBFieldTypeEntry</OPTION>";
              }
           }

           print "      </SELECT>";
           print "    </TH>\n";

           $DBFieldTypeIsSizeless = 'False';
           foreach $SizelessDBFieldTypeEntry (@SizelessDBFieldTypes)
           {
              if ($SizelessDBFieldTypeEntry =~ $AppliedFieldType)
              {
                 $DBFieldTypeIsSizeless = 'True';
              }
           }
           if ($DBFieldTypeIsSizeless =~ 'True')
           {
              print "    <TH><INPUT NAME=\"Applied_Field_Size_$_[3]\" TYPE=\"text\" VALUE=\"Fixed\" SIZE=3 DISABLED></TH>";
           }
           else
           {
              print "    <TH><INPUT NAME=\"Applied_Field_Size_$_[3]\" TYPE=\"text\" VALUE=\"$AppliedFieldSize\" SIZE=3></TH>";
           }

           if ($AppliedFieldAutoIncrement)
           {
              print "    <TH><INPUT NAME=\"Applied_Field_Auto_Increment_$_[3]\" TYPE=\"Checkbox\" VALUE=\"CHECKED\" CHECKED></TH>";
           }
           else
           {
              print "    <TH><INPUT NAME=\"Applied_Field_Auto_Increment_$_[3]\" TYPE=\"Checkbox\" VALUE=\"UNCHECKED\"></TH>";
           }
           if ($AppliedFieldAllowedNull)
           {
              print "    <TH><INPUT NAME=\"Applied_Field_Allowed_Null_$_[3]\" TYPE=\"Checkbox\" VALUE=\"CHECKED\" CHECKED></TH>";
           }
           else
           {
              print "    <TH><INPUT NAME=\"Applied_Field_Allowed_Null_$_[3]\" TYPE=\"Checkbox\" VALUE=\"UNCHECKED\"></TH>";
           }
           print "    <TH bgcolor=\"$RedGrey\"><INPUT NAME=\"Delete_Field_Button_$_[3]\" TYPE=\"Submit\" VALUE=\"Delete Field\" onClick=\"DoConfirm('WARNING\\n\\nYou are about to delete a $MenuElements.\\n\\nDo you want to continue?')\"></TH>";
           print "  </TR>";
           $LoopCounter = (++$LoopCounter);
        }
     }
  }
  # ------------------------------------------------------------------------------------------------------------------

  $AppliedFieldName = $q->param('Applied_Field_Name');

  if ($q->param('Applied_Field_Name'))
  {
     if ( $DebugLevel =~ '^True$' )
     {
        print "Test: New Applied_Field_Name Record Detected<br>\n";
     }

     if ($AppliedFieldName)
     {
        $AppliedFieldPrimaryKey    = $q->param('Applied_Field_Primary_Key');
        $AppliedFieldName          = $q->param('Applied_Field_Name');
        $AppliedFieldType          = $q->param('Applied_Field_Type');
        $AppliedFieldSize          = $q->param('Applied_Field_Size');
        $AppliedFieldAutoIncrement = $q->param('Applied_Field_Auto_Increment');
        $AppliedFieldAllowedNull   = $q->param('Applied_Field_Allowed_Null');

        print "  <TR ALIGN=\"center\" VALIGN=\"center\">";

        if ($AppliedFieldPrimaryKey)
        {
           print "    <TH><INPUT NAME=\"Applied_Field_Primary_Key_$LoopCounter\" TYPE=\"checkbox\" VALUE=\"CHECKED\" CHECKED></TH>";
        }
        else
        {
           print "    <TH><INPUT NAME=\"Applied_Field_Primary_Key_$LoopCounter\" TYPE=\"checkbox\" VALUE=\"UNCHECKED\"></TH>";
        }
        print "    <TH><INPUT NAME=\"Applied_Field_Name_$LoopCounter\" TYPE=\"text\" VALUE=\"$AppliedFieldName\" SIZE=55></TH>";
        print "    <TH>\n";
        print "      <SELECT NAME=\"Applied_Field_Type_$LoopCounter\" SIZE=1>";

           foreach $DBFieldTypeEntry (@DBFieldTypes)
           {
              if ( $DBFieldTypeEntry =~ /^$AppliedFieldType$/ )
              {
                 print "<OPTION SELECTED>$DBFieldTypeEntry</OPTION>";
              }
              else
              {
                 print "<OPTION>$DBFieldTypeEntry</OPTION>";
              }
           }

        print "      </SELECT>";
        print "    </TH>\n";

        $DBFieldTypeIsSizeless = 'False';
        foreach $SizelessDBFieldTypeEntry (@SizelessDBFieldTypes)
        {
           if ($SizelessDBFieldTypeEntry =~ $AppliedFieldType)
           {
              $DBFieldTypeIsSizeless = 'True';
           }
        }
        if ($DBFieldTypeIsSizeless =~ 'True')
        {
           print "    <TH><INPUT NAME=\"Applied_Field_Size_$LoopCounter\" TYPE=\"text\" VALUE=\"Fixed\" SIZE=3 DISABLED></TH>";
        }
        else
        {
           print "    <TH><INPUT NAME=\"Applied_Field_Size_$LoopCounter\" TYPE=\"text\" VALUE=\"$AppliedFieldSize\" SIZE=3></TH>";
        }

        if ($AppliedFieldAutoIncrement)
        {
           print "    <TH><INPUT NAME=\"Applied_Field_Auto_Increment_$LoopCounter\" TYPE=\"Checkbox\" VALUE=\"CHECKED\" CHECKED></TH>";
        }
        else
        {
           print "    <TH><INPUT NAME=\"Applied_Field_Auto_Increment_$LoopCounter\" TYPE=\"Checkbox\" VALUE=\"UNCHECKED\"></TH>";
        }
        if ($AppliedFieldAllowedNull)
        {
           print "    <TH><INPUT NAME=\"Applied_Field_Allowed_Null_$LoopCounter\" TYPE=\"Checkbox\" VALUE=\"CHECKED\" CHECKED></TH>";
        }
        else
        {
           print "    <TH><INPUT NAME=\"Applied_Field_Allowed_Null_$LoopCounter\" TYPE=\"Checkbox\" VALUE=\"UNCHECKED\"></TH>";
        }
        print "    <TH><INPUT NAME=\"Delete_Field_Button_$LoopCounter\" TYPE=\"Submit\" VALUE=\"Delete Field\" onClick=\"DoConfirm('WARNING\\n\\nYou are about to delete a $MenuElements.\\n\\nDo you want to continue?')\"></TH>";

        print "  </TR>";
     }
  }

# ------------------------------------------------------------------------------------------------------------------

  if ( $DebugLevel =~ '^True$' )
  {
     print "Action: New Empty Applied_Field_Name Record writing<br>\n";
  }
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH><INPUT NAME=\"Applied_Field_Primary_Key\" TYPE=\"checkbox\" VALUE=\"UNCHECKED\"></TH>";
  print "    <TH><INPUT NAME=\"Applied_Field_Name\" TYPE=\"text\" VALUE=\"\" SIZE=55></TH>";
  print "    <TH>\n";
  print "      <SELECT NAME=\"Applied_Field_Type\" SIZE=1>";
  foreach $DBFieldTypeEntry (@DBFieldTypes)
  {
     print "        <OPTION>$DBFieldTypeEntry</OPTION>";
  }
  print "      </SELECT>";
  print "    </TH>\n";
  print "    <TH><INPUT NAME=\"Applied_Field_Size\" TYPE=\"text\" VALUE=\"20\" SIZE=3></TH>";
  print "    <TH><INPUT NAME=\"Applied_Field_Auto_Increment\" TYPE=\"Checkbox\" VALUE=\"UNCHECKED\"></TH>";
  print "    <TH><INPUT NAME=\"Applied_Field_Allowed_Null\" TYPE=\"Checkbox\" VALUE=\"CHECKED\" CHECKED></TH>";
  print "    <TH bgcolor=\"$RedGrey\"><INPUT NAME=\"Delete_Field_Button\" TYPE=\"Submit\" VALUE=\"Delete Field\" onClick=\"DoConfirm('WARNING\\n\\nYou are about to delete a $MenuElements.\\n\\nDo you want to continue?')\"></TH>";
  print "  </TR>";

  print "</TABLE>";
  print "</FORM>";
}

# ==================================================================================================================

sub Records_Menu
{
  if ( $DebugLevel =~ '^True$' )
  {
     print "Form_Phase: Records_Menu Started<br>\n";
  }
  $PageRecordsLimit = 1000;

  $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost","$AppliedUsername","$AppliedPassword") or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth = $dbh->prepare( "SELECT COUNT(*) FROM $SelectedTable" ) or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth->execute  or warn $DBI::errstr; # Oh, tough luck
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $TotalRecordsCount = $sth->fetchrow_array();
  #$dbh->disconnect or warn $DBI::errstr;

  if ($TotalRecordsCount > $PageRecordsLimit)
  {
     $OffsetEnabled = 'True';
     foreach $ParamEntry ($q->param)
     {
        if ($q->param($ParamEntry))
        {
           if ($ParamEntry =~ /^Generic_Action_Previous$/)
           {
              $PreviousPageRecordsOffsetValue = $q->param('Page_Records_Offset');
              $PageRecordsOffsetValue = $PreviousPageRecordsOffsetValue - $PageRecordsLimit;
              if ($PageRecordsOffsetValue < 0) { $PageRecordsOffsetValue = 0; }
              $LimitClauseSQLString = "LIMIT $PageRecordsOffsetValue,$PageRecordsLimit";
           }
           elsif ($ParamEntry =~ /^Generic_Action_Next$/)
           {
              $PreviousPageRecordsOffsetValue = $q->param('Page_Records_Offset');
              $PageRecordsOffsetValue = $PreviousPageRecordsOffsetValue + $PageRecordsLimit;
              $LimitClauseSQLString = "LIMIT $PageRecordsOffsetValue,$PageRecordsLimit";
           }
           else
           {
              $PageRecordsOffsetFound = 'False';
              foreach $ParamEntry ($q->param)
              {
                 if ($q->param($ParamEntry))
                 {
                    if ($ParamEntry =~ /^Page_Records_Offset$/)
                    {
                       $PageRecordsOffsetFound = 'True';
                    }
                 }
              }
              if ($PageRecordsOffsetFound =~ m/^True$/)
              {
                 $PageRecordsOffsetValue = $q->param('Page_Records_Offset');
                 $LimitClauseSQLString = "LIMIT $PageRecordsOffsetValue,$PageRecordsLimit";
              }
              else
              {
                 $PageRecordsOffsetValue = 0;
                 $LimitClauseSQLString = "LIMIT $PageRecordsOffsetValue,$PageRecordsLimit";
              }
           }
        }
     }
     if ($PageRecordsOffsetValue <= 0)
     {
        $GenericActionPreviousDescription = 'Previous Page';
        $GenericActionPreviousDisabled = 'DISABLED';
     }
     else
     {
        $GenericActionPreviousDescription = 'Previous Page';
        $GenericActionPreviousDisabled = '';
     }

     $EndOffPageRecordsOffsetValue = $PageRecordsOffsetValue + $PageRecordsLimit;
     if ($EndOffPageRecordsOffsetValue > $TotalRecordsCount)
     {
        $GenericActionNextDescription = 'Next Page';
        $GenericActionNextDisabled = 'DISABLED';
     }
     else
     {
        $GenericActionNextDescription = 'Next Page';
        $GenericActionNextDisabled = '';
     }
  }
  else
  {
     $GenericActionPreviousDescription = 'Previous Page';
     $GenericActionPreviousDisabled = 'DISABLED';
     $GenericActionNextDescription = 'Next Page';
     $GenericActionNextDisabled = 'DISABLED';
  }

  $PageRecordsOffsetValueToShow = ( $PageRecordsOffsetValue + 1 );
  $EndOffPageRecordsOffsetValueToShow = ( $EndOffPageRecordsOffsetValue + 0);
  $TotalRecordsCountToShow = ($TotalRecordsCount + 0 );
  $SelectedRecords = "$PageRecordsOffsetValueToShow-$EndOffPageRecordsOffsetValueToShow of $TotalRecordsCountToShow";

  $NavigationBarMenu = 'Records_Menu';
# $SelectedHost = '';
# $SelectedDBEnv = '';
# $SelectedDatabase = '';
# $SelectedTable = '';
# $AppliedUsername = '';
# $AppliedPassword = '';

  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionAddDescription = 'Add Record';
  $GenericActionAddDisabled = '';
  if (( $SelectedDBEnv =~ m/^mysql$/ ) and ( $SelectedDatabase =~ m/^mysql$/ )) { $GenericActionRefreshDescription = 'Refresh (Privileges)'; }
  else { $GenericActionRefreshDescription = 'Refresh'; }
  $GenericActionRefreshDisabled = '';

  $SelectedHost = $q->param('Selected_Host');
  $SelectedDBEnv = $q->param('Selected_DB_Env');
  $SelectedDatabase = $q->param('Selected_Database');
  $AppliedUsername = $q->param('Applied_Username');
  $AppliedPassword = $q->param('Applied_Password');

  $RecordsMenuSQLString = "SELECT * FROM $SelectedTable";

  $OrderByClauseSQLString = "";

  foreach $ParamEntry ($q->param)
  {
     if ($q->param($ParamEntry))
     {
        if ($ParamEntry =~ m/^Sort_Column_Button_/)
        {
           $_ = $ParamEntry;
           s/^Sort_Column_Button_//;
           $ColumnToSort = $_;
           $OrderByClauseSQLString = "ORDER BY $ColumnToSort";
        }
     }
  }

  $RecordsMenuSQLString .= " $OrderByClauseSQLString";
  $RecordsMenuSQLString .= " $LimitClauseSQLString";

  print "<FORM NAME=\"Generic_Form\" METHOD=\"POST\">";

  print "<INPUT TYPE=\"hidden\" NAME=\"Form_Phase\"    VALUE=\"Records_Menu\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Host\"    VALUE=\"",$q->param('Selected_Host'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_DB_Env\"  VALUE=\"",$q->param('Selected_DB_Env'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Username\" VALUE=\"",$q->param('Applied_Username'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Password\" VALUE=\"",$q->param('Applied_Password'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Database\"  VALUE=\"$SelectedDatabase\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Table\"  VALUE=\"$SelectedTable\">\n";

  if ($OffsetEnabled =~ m/^True$/)
  {
     print "<INPUT TYPE=\"hidden\" NAME=\"Page_Records_Offset\"  VALUE=\"$PageRecordsOffsetValue\">\n";
  }

  Display_Navigation_Bar();

# -------------------- START TABLE --------------------

  print "<TABLE  width=\"100%\" ALIGN=\"center\" BORDER=\"1\" bgcolor=\"$Grey\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor = \"$SoftBlue\"COLSPAN = 200><font color=\"$White\"><big><big>$NavigationBarMenu</big></big></font></TH>";
  print "  </TR>";

# -------------- START HEADER FIELDS LOOP -------------

# Well, this loop, loops until it reaches the last field as the fieldnames in the header of the table

  #$dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost","$AppliedUsername","$AppliedPassword") or warn $DBI::errstr;
  $sth = $dbh->prepare( "DESCRIBE $SelectedTable" ) or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth->execute  or warn $DBI::errstr; # Oh, tough luck
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

  $LoopCounter = 0;
  while ( @FieldAttributes = $sth->fetchrow_array())
  {
     if (@FieldAttributes) {
        $FieldNames[$LoopCounter]    = $FieldAttributes[0];
        $FieldTypes[$LoopCounter]    = $FieldAttributes[1];
        $FieldNulls[$LoopCounter]    = $FieldAttributes[2];
        $FieldKeys[$LoopCounter]     = $FieldAttributes[3];
        $FieldDefaults[$LoopCounter] = $FieldAttributes[4];
        $FieldExtras[$LoopCounter]   = $FieldAttributes[5];
        $LoopCounter = (++$LoopCounter);
     }
  }

  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Name</font></TH>";
  foreach $FieldNameEntry (@FieldNames) { print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">$FieldNameEntry</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Type</font></TH>";
  foreach $FieldTypeEntry (@FieldTypes) { print "    <TH bgcolor=\"$DarkGray\"><font color=\"$UltraDarkGrey\">$FieldTypeEntry</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Null</font></TH>";
  foreach $FieldNullsEntry (@FieldNulls) { if ($FieldNullsEntry) { print "    <TH><INPUT NAME=\"FieldNullsEntry\" TYPE=\"checkbox\" VALUE=\"CHECKED\" CHECKED DISABLED></TH>"; }
  else { print "    <TH><INPUT NAME=\"FieldNullsEntry\" TYPE=\"checkbox\" VALUE=\"CHECKED\" DISABLED></TH>"; }}
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Key</font></TH>";
  foreach $FieldKeysEntry (@FieldKeys) { print "    <TH bgcolor=\"$Gray\"><font color=\"$UltraDarkGrey\">$FieldKeysEntry&nbsp</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Defaults</font></TH>";
  foreach $FieldDefaultsEntry (@FieldDefaults) { print "    <TH bgcolor=\"$Gray\"><font color=\"$UltraDarkGrey\">$FieldDefaultsEntry&nbsp</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Extra</font></TH>";
  foreach $FieldExtrasEntry (@FieldExtras) { print "    <TH bgcolor=\"$Gray\"><font color=\"$UltraDarkGrey\">$FieldExtrasEntry&nbsp</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$Black\"><font color=\"$Orange\">Count</font></TH>";
  foreach $FieldNameEntry (@FieldNames)
  {
     if ($ColumnToSort =~ $FieldNameEntry)
     {
        print "    <TH bgcolor=\"$Green\"><INPUT NAME=\"Sort_Column_Button_$FieldNameEntry\" TYPE=\"Submit\" VALUE=\"$FieldNameEntry\"></TH>";
     }
     else
     {
        print "    <TH bgcolor=\"$DarkBlue\"><INPUT NAME=\"Sort_Column_Button_$FieldNameEntry\" TYPE=\"Submit\" VALUE=\"$FieldNameEntry\"></TH>";
     }
  }
  print "<TH bgcolor=\"$Black\"><font color=\"$Orange\">Action</font></TH>";
  print "<TH bgcolor=\"$Black\"><font color=\"$Red\">Action</font></TH>";
  print "  </TR>";

# ----------------- START RECORDS LOOP ----------------
  $RecordsLoopCounter = 0;
  $FieldsLoopCounter = 0;

  if ( $DebugLevel =~ '^True$' )
  {
     print "Action: Executing SQL string: $RecordsMenuSQLString<br>\n";
  }

  $sth = $dbh->prepare( "$RecordsMenuSQLString" ) or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth->execute  or warn $DBI::errstr; # Oh, tough luck
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  while ( @RecordFields = $sth->fetchrow_array())
  {
     print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
     $RecordsLoopCounterToShow = $RecordsLoopCounter + $PageRecordsOffsetValue +1;
     print "    <TH bgcolor=\"$OrangeGrey\">$RecordsLoopCounterToShow</TH>";
     $FieldsLoopCounter = 0;
     $IdentifierString = "";
     foreach $RecordFieldEntry (@RecordFields)
     {
        $Records[$FieldsLoopCounter] = $RecordEntry[0];
        print "    <TD bgcolor=\"$Grey\">$RecordFieldEntry</TD>";
        $IdentifierString .= "BeGiN$FieldNames[$FieldsLoopCounter]BeTwEeN$RecordFieldEntry";
        $FieldsLoopCounter = (++$FieldsLoopCounter);
     }
     print "    <TH bgcolor=\"$OrangeGrey\"><INPUT NAME=\"Edit_Record_Button_$IdentifierString\" TYPE=\"Submit\" VALUE=\"Edit\"></TH>";
     print "    <TH bgcolor=\"$RedGrey\"><INPUT NAME=\"Delete_Record_Button_$IdentifierString\" TYPE=\"Submit\" VALUE=\"Delete\" onClick=\"DoConfirm('WARNING\\n\\nYou are about to delete a $MenuElement.\\n\\nDo you want to continue?')\"></TH>";

     print "  </TR>";
     $RecordsLoopCounter = (++$RecordsLoopCounter);
  }
  $dbh->disconnect or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  print "</TABLE>";
  print "</FORM>";
}

# ==================================================================================================================

sub Records_Menu_Add_Record
{
  if ( $DebugLevel =~ '^True$' )
  {
     print "Form_Phase: Records_Menu_Add_Record Started<br>\n";
  }

  $NavigationBarMenu = 'Records_Menu_Add_Record';
  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionAddDescription = 'Disabled';
  $GenericActionAddDisabled = 'DISABLED';
  $GenericActionRefreshDescription = 'Refresh';
  $GenericActionRefreshDisabled = '';
  $GenericActionPreviousDescription = 'Previous Page';
  $GenericActionPreviousDisabled = 'DISABLED';
  $GenericActionNextDescription = 'Next Page';
  $GenericActionNextDisabled = 'DISABLED';

  $SelectedHost = $q->param('Selected_Host');
  $SelectedDBEnv = $q->param('Selected_DB_Env');
  $SelectedDatabase = $q->param('Selected_Database');
  $SelectedTable = $q->param('Selected_Table');
  $AppliedUsername = $q->param('Applied_Username');
  $AppliedPassword = $q->param('Applied_Password');

  if ( $DebugLevel =~ '^True$' )
  {
     print "Started Records_Menu_Add_Record<br>\n";
  }

  print "<FORM NAME=\"Generic_Form\" METHOD=\"POST\">";

  print "<INPUT TYPE=\"hidden\" NAME=\"Form_Phase\"    VALUE=\"Records_Menu_Add_Record\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Host\"    VALUE=\"",$q->param('Selected_Host'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_DB_Env\"  VALUE=\"",$q->param('Selected_DB_Env'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Username\" VALUE=\"",$q->param('Applied_Username'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Password\" VALUE=\"",$q->param('Applied_Password'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Database\"  VALUE=\"$SelectedDatabase\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Table\"  VALUE=\"$SelectedTable\">\n";

  Display_Navigation_Bar();

# -------------------- START TABLE --------------------

  print "<TABLE  width=\"100%\" ALIGN=\"center\" BORDER=\"1\" bgcolor=\"$Grey\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor = \"$SoftBlue\"COLSPAN = 200><font color=\"$White\"><big><big>$NavigationBarMenu</big></big></font></TH>";
  print "  </TR>";

# -------------- START HEADER FIELDS LOOP -------------

  $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost","$AppliedUsername","$AppliedPassword") or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth = $dbh->prepare( "DESCRIBE $SelectedTable" ) or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth->execute  or warn $DBI::errstr; # Oh, tough luck
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

  $LoopCounter = 0;
  while ( @FieldAttributes = $sth->fetchrow_array())
  {
     if (@FieldAttributes) {
        $FieldNames[$LoopCounter]    = $FieldAttributes[0];
        $FieldTypes[$LoopCounter]    = $FieldAttributes[1];
        $FieldNulls[$LoopCounter]    = $FieldAttributes[2];
        $FieldKeys[$LoopCounter]     = $FieldAttributes[3];
        $FieldDefaults[$LoopCounter] = $FieldAttributes[4];
        $FieldExtras[$LoopCounter]   = $FieldAttributes[5];
        $LoopCounter = (++$LoopCounter);
     }
  }
  $dbh->disconnect or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Name</font></TH>";
  foreach $FieldNameEntry (@FieldNames) { print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">$FieldNameEntry</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Type</font></TH>";
  foreach $FieldTypeEntry (@FieldTypes) { print "    <TH bgcolor=\"$DarkGray\"><font color=\"$UltraDarkGrey\">$FieldTypeEntry</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Null</font></TH>";
  foreach $FieldNullsEntry (@FieldNulls) { if ($FieldNullsEntry) { print "    <TH><INPUT NAME=\"FieldNullsEntry\" TYPE=\"checkbox\" VALUE=\"CHECKED\" CHECKED DISABLED></TH>"; }
  else { print "    <TH><INPUT NAME=\"FieldNullsEntry\" TYPE=\"checkbox\" VALUE=\"CHECKED\" DISABLED></TH>"; }}
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Key</font></TH>";
  foreach $FieldKeysEntry (@FieldKeys) { print "    <TH bgcolor=\"$Gray\"><font color=\"$UltraDarkGrey\">$FieldKeysEntry&nbsp</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Defaults</font></TH>";
  foreach $FieldDefaultsEntry (@FieldDefaults) { print "    <TH bgcolor=\"$Gray\"><font color=\"$UltraDarkGrey\">$FieldDefaultsEntry&nbsp</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Extra</font></TH>";
  foreach $FieldExtrasEntry (@FieldExtras) { print "    <TH bgcolor=\"$Gray\"><font color=\"$UltraDarkGrey\">$FieldExtrasEntry&nbsp</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Name</font></TH>";
  foreach $FieldNameEntry (@FieldNames) { print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">$FieldNameEntry</TH>"; }
  print "<TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  print "  </TR>";

# ----------------- START RECORDS LOOP ----------------

  $LoopCounter = 0;

  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">Record</font></TH>";
  foreach $FieldTypeEntry (@FieldTypes)
  {
     $_ = $FieldTypeEntry;
     s/[^0-9]+//;
     s/[^0-9]+//;
     $FieldTypeEntrySize = $_;
     print "    <TH><INPUT NAME=\"Applied_Insert_Record_Field_$FieldNames[$LoopCounter]\" TYPE=\"text\" VALUE=\"\" SIZE=20 MAXLENGTH=\"$FieldTypeEntrySize\" ></TH>";
     $LoopCounter = (++$LoopCounter);
  }

  print "    <TH bgcolor=\"$OrangeGrey\"><INPUT NAME=\"Insert_Record_Button\" TYPE=\"Submit\" VALUE=\"Insert\"></TH>";
  print "  </TR>";
  print "</TABLE>";
  print "</FORM>";
}

# ==================================================================================================================

sub Records_Menu_Edit_Record
{
  if ( $DebugLevel =~ '^True$' )
  {
     print "Form_Phase: Records_Menu_Edit_Record Started<br>\n";
  }

  $NavigationBarMenu = 'Records_Menu_Edit_Record';
  $GenericActionBackDescription = 'Back';
  $GenericActionBackDisabled = '';
  $GenericActionAddDescription = 'Disabled';
  $GenericActionAddDisabled = 'DISABLED';
  $GenericActionRefreshDescription = 'Disabled';
  $GenericActionRefreshDisabled = 'DISABLED';
  $GenericActionPreviousDescription = 'Previous Page';
  $GenericActionPreviousDisabled = 'DISABLED';
  $GenericActionNextDescription = 'Next Page';
  $GenericActionNextDisabled = 'DISABLED';

  $SelectedHost = $q->param('Selected_Host');
  $SelectedDBEnv = $q->param('Selected_DB_Env');
  $SelectedDatabase = $q->param('Selected_Database');
  $SelectedTable = $q->param('Selected_Table');
  $AppliedUsername = $q->param('Applied_Username');
  $AppliedPassword = $q->param('Applied_Password');

  if ( $DebugLevel =~ '^True$' )
  {
     print "Started Records_Menu_Edit_Record<br>\n";
  }

  print "<FORM NAME=\"Generic_Form\" METHOD=\"POST\">";

  print "<INPUT TYPE=\"hidden\" NAME=\"Form_Phase\"    VALUE=\"Records_Menu_Edit_Record\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Host\"    VALUE=\"",$q->param('Selected_Host'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_DB_Env\"  VALUE=\"",$q->param('Selected_DB_Env'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Username\" VALUE=\"",$q->param('Applied_Username'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Applied_Password\" VALUE=\"",$q->param('Applied_Password'),"\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Database\"  VALUE=\"$SelectedDatabase\">\n";
  print "<INPUT TYPE=\"hidden\" NAME=\"Selected_Table\"  VALUE=\"$SelectedTable\">\n";

  Display_Navigation_Bar();

# -------------------- START TABLE --------------------

  print "<TABLE  width=\"100%\" ALIGN=\"center\" BORDER=\"1\" bgcolor=\"$Grey\">";
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor = \"$SoftBlue\"COLSPAN = 200><font color=\"$White\"><big><big>$NavigationBarMenu</big></big></font></TH>";
  print "  </TR>";

# -------------- START HEADER FIELDS LOOP -------------

  $dbh = DBI->connect("dbi\:$SelectedDBEnv\:$SelectedDatabase\:$SelectedHost","$AppliedUsername","$AppliedPassword") or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth = $dbh->prepare( "DESCRIBE $SelectedTable" ) or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}
  $sth->execute  or warn $DBI::errstr; # Oh, tough luck
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

  $LoopCounter = 0;
  while ( @FieldAttributes = $sth->fetchrow_array())
  {
     if (@FieldAttributes) {
        $FieldNames[$LoopCounter]    = $FieldAttributes[0];
        $FieldTypes[$LoopCounter]    = $FieldAttributes[1];
        $FieldNulls[$LoopCounter]    = $FieldAttributes[2];
        $FieldKeys[$LoopCounter]     = $FieldAttributes[3];
        $FieldDefaults[$LoopCounter] = $FieldAttributes[4];
        $FieldExtras[$LoopCounter]   = $FieldAttributes[5];
        $LoopCounter = (++$LoopCounter);
     }
  }
  $dbh->disconnect or warn $DBI::errstr;
  $ErrorString = $DBI::errstr; if ($ErrorString) { Error_Message($ErrorString);}

  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Name</font></TH>";
  foreach $FieldNameEntry (@FieldNames) { print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">$FieldNameEntry</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Type</font></TH>";
  foreach $FieldTypeEntry (@FieldTypes) { print "    <TH bgcolor=\"$DarkGray\"><font color=\"$UltraDarkGrey\">$FieldTypeEntry</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Null</font></TH>";
  foreach $FieldNullsEntry (@FieldNulls) { if ($FieldNullsEntry) { print "    <TH><INPUT NAME=\"FieldNullsEntry\" TYPE=\"checkbox\" VALUE=\"CHECKED\" CHECKED DISABLED></TH>"; }
  else { print "    <TH><INPUT NAME=\"FieldNullsEntry\" TYPE=\"checkbox\" VALUE=\"CHECKED\" DISABLED></TH>"; }}
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Key</font></TH>";
  foreach $FieldKeysEntry (@FieldKeys) { print "    <TH bgcolor=\"$Gray\"><font color=\"$UltraDarkGrey\">$FieldKeysEntry&nbsp</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Defaults</font></TH>";
  foreach $FieldDefaultsEntry (@FieldDefaults) { print "    <TH bgcolor=\"$Gray\"><font color=\"$UltraDarkGrey\">$FieldDefaultsEntry&nbsp</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR BGCOLOR=\"$DarkGrey\" ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Extra</font></TH>";
  foreach $FieldExtrasEntry (@FieldExtras) { print "    <TH bgcolor=\"$Gray\"><font color=\"$UltraDarkGrey\">$FieldExtrasEntry&nbsp</TH>"; }
  print "    <TH COLSPAN=2 bgcolor=\"$SoftBlue\"><font color=\"$Blue\">&nbsp</FONT></TH>";
  print "  </TR>";

  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$SoftBlue\"><font color=\"$Yellow\">Name</font></TH>";
  foreach $FieldNameEntry (@FieldNames) { print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">$FieldNameEntry</TH>"; }
  print "<TH bgcolor=\"$Black\"><font color=\"$Green\">Action</font></TH>";
  print "  </TR>";

# ----------------- START RECORDS LOOP ----------------

  foreach $ParamEntry ($q->param)
  {
     if ($q->param($ParamEntry))
     {
        if ($ParamEntry =~ '^Edit_Record_Button_.*')
        {
           $EditRecordIdentifierString = $ParamEntry;
        }
     }
  }

  $_ = $EditRecordIdentifierString;
  @IdentifierFieldPairs = split /BeGiN/, $EditRecordIdentifierString;
  $LoopCounter = 0;
  foreach $IdentifierFieldPairsEntry (@IdentifierFieldPairs)
  {
     if ($IdentifierFieldPairsEntry !~ /^Edit_Record_Button_$/ )
     {
        $IdentifierFieldNames[$LoopCounter] = $IdentifierFieldPairsEntry;
        $_ = $IdentifierFieldNames[$LoopCounter]; s/BeTwEeN.*//; $IdentifierFieldNames[$LoopCounter] = $_;
        $IdentifierFieldValues[$LoopCounter] = $IdentifierFieldPairsEntry;
        $_ = $IdentifierFieldValues[$LoopCounter]; s/.*BeTwEeN//; $IdentifierFieldValues[$LoopCounter] = $_;
        if ( $DebugLevel =~ /^True$/ )
        {
           print "$IdentifierFieldNames[$LoopCounter] = $IdentifierFieldValues[$LoopCounter]<br>\n";
        }
        $LoopCounter = (++$LoopCounter);
     }
  }

  $LoopCounter = 0;
  print "  <TR ALIGN=\"center\" VALIGN=\"center\">";
  print "    <TH bgcolor=\"$DarkBlue\"><font color=\"$Yellow\">Record</font></TH>";
  foreach $FieldTypeEntry (@FieldTypes)
  {
     $_ = $FieldTypeEntry;
     s/[^0-9]+//;
     s/[^0-9]+//;
     $FieldTypeEntrySize = $_;
     print "    <TH><INPUT NAME=\"Applied_Update_Record_Field_$FieldNames[$LoopCounter]\" TYPE=\"TEXT\" VALUE=\"$IdentifierFieldValues[$LoopCounter]\" SIZE=20 MAXLENGTH=\"$FieldTypeEntrySize\" ></TH>";
     $LoopCounter = (++$LoopCounter);
  }

  print "    <TH bgcolor=\"$OrangeGrey\"><INPUT NAME=\"Update_Record_Button_$EditRecordIdentifierString\" TYPE=\"Submit\" VALUE=\"Update\"></TH>";
  print "  </TR>";
  print "</TABLE>";
  print "</FORM>";
}