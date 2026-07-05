# Add steps/actions here:

1. Replacing in main.tf from 
  variable "files" {
  default = 5
}

to 

variable "files" {
  default = [
    "file0.txt",
    "file1.txt",
    "file2.txt",
    "file3.txt",
    "file4.txt"
  ]
}

2. Replace 'count' with 'for_each'

Update the resouce definition:

 resource "local_file" "foo" {
   for_each = toset(var.files)

 filename = each.key
 content = "#Some Content for ${replace(each.key,".txt", "")}"
 }

3. Map the existing resources from indexed addresses to keyed addresses using 'terraform state mv'

 terraform state mv'local_file.foo[0]''local_file.foo["file0.txt"]'
 terraform state mv'local_file.foo[0]''local_file.foo["file1.txt"]'
 terraform state mv'local_file.foo[0]''local_file.foo["file2.txt"]'
 terraform state mv'local_file.foo[0]''local_file.foo["file3.txt"]'
 terraform state mv'local_file.foo[0]''local_file.foo["file4.txt"]'

4. Remove te second resource (file1.txt)
 
 variable "files"{
    default = [
     "file0.txt",
     "file1.txt",
     "file2.txt",
     "file3.txt"
     "file4.txt"
    ]

 }

 5. terraform plan

 6. terraform apply