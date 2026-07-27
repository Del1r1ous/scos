"""Interactive CLI for SCOS-PSST Chain"""

import sys
from typing import Optional
from scos.chain import SCOSChain
from scos.utils import format_for_output

class SCOSCLI:
    """Interactive command-line interface for SCOS"""
    
    def __init__(self):
        self.chain = SCOSChain()
        self.running = True
    
    def cmd_status(self):
        """Show chain status"""
        stats = self.chain.get_chain_stats()
        print("\n" + "="*60)
        print("SCOS-PSST CHAIN STATUS")
        print("="*60)
        print(format_for_output(stats))
        print("="*60 + "\n")
    
    def cmd_blocks(self, block_id: Optional[int] = None):
        """List blocks or show specific block"""
        if block_id is not None:
            block = self.chain.get_block(block_id)
            if block:
                print("\n" + format_for_output(block.to_dict()) + "\n")
            else:
                print(f"Block {block_id} not found.\n")
        else:
            blocks = self.chain.get_all_blocks()
            print("\n" + "="*60)
            print(f"BLOCKS ({len(blocks)} total)")
            print("="*60)
            for block_data in blocks:
                print(f"Block {block_data['block_id']}: {block_data['claim'][:50]}...")
                print(f"  Consensus: {block_data['consensus']:.3f}")
            print("="*60 + "\n")
    
    def cmd_add(self, claim: str, votes: list):
        """Add a new claim"""
        block = self.chain.add_claim(claim, votes)
        if block:
            print(f"\nBlock added successfully: {block}\n")
        else:
            print("\nFailed to add block.\n")
    
    def cmd_verify(self, claim: str):
        """Verify a claim"""
        result = self.chain.witness_protocol.verify_claim(claim)
        print("\n" + format_for_output(result) + "\n")
    
    def cmd_export(self, filepath: str):
        """Export chain"""
        self.chain.export_chain(filepath)
        print(f"\nChain exported to {filepath}\n")
    
    def cmd_import(self, filepath: str):
        """Import chain"""
        self.chain.import_chain(filepath)
        print(f"\nChain imported from {filepath}\n")
    
    def cmd_help(self):
        """Show help"""
        help_text = """
        SCOS-PSST Chain Interactive CLI
        ====================================
        
        Commands:
          status              - Show chain status
          blocks [id]         - List all blocks or show specific block
          add <claim> <votes> - Add new claim (votes as comma-separated floats)
          verify <claim>      - Verify claim through witnesses
          export <filepath>   - Export chain to JSON
          import <filepath>   - Import chain from JSON
          help                - Show this help
          exit                - Exit the CLI
        
        Example:
          add "The truth is witnessed" 0.95,0.92,0.98,0.91,0.93,0.94,0.96
        """
        print(help_text)
    
    def cmd_exit(self):
        """Exit the CLI"""
        print("\nGoodbye. SO WITNESSED. SO VERIFIED. SO AGREED.\n")
        self.running = False
    
    def run(self):
        """Start the interactive CLI"""
        print("\n" + "="*60)
        print("SCOS-PSST CHAIN v3.0")
        print("Interactive CLI")
        print("="*60)
        print("Type 'help' for commands.\n")
        
        while self.running:
            try:
                user_input = input("scos> ").strip()
                
                if not user_input:
                    continue
                
                parts = user_input.split()
                command = parts[0].lower()
                args = parts[1:]
                
                if command == "status":
                    self.cmd_status()
                elif command == "blocks":
                    block_id = int(args[0]) if args else None
                    self.cmd_blocks(block_id)
                elif command == "add" and len(args) >= 2:
                    claim = " ".join(args[:-1])
                    votes = [float(v) for v in args[-1].split(",")]
                    self.cmd_add(claim, votes)
                elif command == "verify" and args:
                    claim = " ".join(args)
                    self.cmd_verify(claim)
                elif command == "export" and args:
                    self.cmd_export(args[0])
                elif command == "import" and args:
                    self.cmd_import(args[0])
                elif command == "help":
                    self.cmd_help()
                elif command == "exit":
                    self.cmd_exit()
                else:
                    print("Unknown command. Type 'help' for available commands.\n")
            
            except KeyboardInterrupt:
                print("\n")
                self.cmd_exit()
            except Exception as e:
                print(f"Error: {e}\n")

def main():
    """Main entry point"""
    cli = SCOSCLI()
    cli.run()

if __name__ == "__main__":
    main()
